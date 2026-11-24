#!/usr/bin/env python3
"""Dumm-E's social behaviours, driven by voice commands and the person detector.

  "hi"     -> turn to face the person (if one is in view) and wave
  "dumme"  -> look at the person and follow them for `track_time` seconds;
              if nobody is in view, sweep the base around to search for them
  "record" -> lock the arm where it is and record the camera to a video file
              (ignores "hi"/"dumme" until released)
  "release"-> stop recording and unlock

Subscribes:
  /voice/command          (std_msgs/String)            "hi" | "dumme" | "record" | "release"
  /person_detector/target (geometry_msgs/PointStamped)  angles of the closest person
  /joint_states           (sensor_msgs/JointState)
Publishes:
  /arm_controller/joint_trajectory (trajectory_msgs/JointTrajectory)
  ~/state                          (std_msgs/String)  idle | search | track | wave | record
Calls:
  /video_recorder/record (std_srvs/SetBool)

Looking = pan with the base joint and tilt with the wrist joint, from the
`look_pose` (arm up, wrist folded back so the camera faces forward). The signs
match the upright image the person detector reports in (image_rotation 90).
"""
import math

import rclpy
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import PointStamped
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from std_srvs.srv import SetBool
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

JOINTS = ["shoulder_rotation_plate_joint", "shoulder_joint", "elbow_joint", "wrist_joint"]
PAN, ELBOW, WRIST = 0, 2, 3
LIMIT = math.pi - 0.1  # stay off the +-pi joint limits (Gazebo glitches against them)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def duration(t):
    return Duration(sec=int(t), nanosec=int((t - int(t)) * 1e9))


class Behavior(Node):
    def __init__(self):
        super().__init__("behavior")
        # shoulder 75 deg, elbow 0, wrist 165 deg: camera ~0.46 m up, looking forward, 11 deg up
        self.declare_parameter("look_pose", [0.0, 1.309, 0.0, 2.880])
        self.declare_parameter("pan_limit", 2.6)        # rad either side of 0
        self.declare_parameter("tilt_range", 0.8)       # wrist travel around look_pose, rad
        self.declare_parameter("gain", 0.6)             # fraction of the angle error fixed per frame
        self.declare_parameter("deadband", 0.03)        # rad
        self.declare_parameter("search_speed", 0.6)     # rad/s
        self.declare_parameter("track_time", 20.0)      # s to keep following after "dumme"
        self.declare_parameter("lost_timeout", 2.5)     # s without a person before searching
        self.declare_parameter("wave_swing", [0.25, 0.35])  # pan, elbow amplitude (rad)
        self.declare_parameter("wave_period", 1.2)      # s per wave (stretched to max_speed)
        self.declare_parameter("wave_count", 3)
        # URDF joint velocity limit is 1 rad/s; going faster makes Gazebo's
        # position loop overshoot and stick, and is rough on real servos.
        self.declare_parameter("max_speed", 0.9)        # rad/s per joint

        p = lambda n: self.get_parameter(n).value  # noqa: E731
        self.look = list(p("look_pose"))
        self.pan_limit = float(p("pan_limit"))
        self.tilt_lo = self.look[WRIST] - float(p("tilt_range"))
        self.tilt_hi = min(LIMIT, self.look[WRIST] + float(p("tilt_range")))
        self.gain = float(p("gain"))
        self.deadband = float(p("deadband"))
        self.search_speed = float(p("search_speed"))
        self.track_time = float(p("track_time"))
        self.lost_timeout = float(p("lost_timeout"))
        self.wave_swing = list(p("wave_swing"))
        self.wave_period = float(p("wave_period"))
        self.wave_count = int(p("wave_count"))
        self.max_speed = float(p("max_speed"))

        self.joints = None         # measured positions
        self.cmd = None            # last commanded positions
        self.state = "idle"
        self.track_until = 0.0
        self.target = None         # (x, y) angles of the latest person
        self.target_time = -1e9
        self.wave_end = 0.0
        self.after_wave = "idle"
        self.sweep_dir = 1.0
        self.sweep_turns = 0

        self.traj_pub = self.create_publisher(JointTrajectory, "/arm_controller/joint_trajectory", 10)
        self.state_pub = self.create_publisher(String, "~/state", 10)
        self.create_subscription(JointState, "/joint_states", self.on_joints, 10)
        self.create_subscription(String, "/voice/command", self.on_command, 10)
        self.create_subscription(PointStamped, "/person_detector/target", self.on_target, 10)
        self.recorder = self.create_client(SetBool, "/video_recorder/record")
        self.create_timer(0.1, self.tick)
        self.get_logger().info(
            'Ready: "hi" = wave, "dummy" = look at me, "start recording" / "release" = lock + record'
        )

    # ---------------------------------------------------------------- helpers
    def now(self):
        return self.get_clock().now().nanoseconds * 1e-9

    def send(self, points):
        """points: [(positions, min_segment_seconds), ...]

        Each segment is stretched if needed so no joint exceeds max_speed.
        Returns the total duration.
        """
        msg = JointTrajectory(joint_names=JOINTS)
        prev, t = self.cmd, 0.0
        for pos, dt in points:
            step = max(abs(a - b) for a, b in zip(pos, prev))
            t += max(dt, step / self.max_speed)
            msg.points.append(JointTrajectoryPoint(positions=list(pos), time_from_start=duration(t)))
            prev = pos
        self.traj_pub.publish(msg)
        self.cmd = list(points[-1][0])
        return t

    def set_state(self, state):
        if state != self.state:
            self.get_logger().info(f"{self.state} -> {state}")
            self.state = state
        self.state_pub.publish(String(data=state))

    def person_visible(self):
        return self.now() - self.target_time < 0.6

    def look_at(self, pan, tilt, t):
        pose = list(self.look)
        pose[PAN] = clamp(pan, -self.pan_limit, self.pan_limit)
        pose[WRIST] = clamp(tilt, self.tilt_lo, self.tilt_hi)
        self.send([(pose, t)])

    # -------------------------------------------------------------- callbacks
    def on_joints(self, msg: JointState):
        pos = dict(zip(msg.name, msg.position))
        if not all(j in pos for j in JOINTS):
            return
        first = self.joints is None
        self.joints = [pos[j] for j in JOINTS]
        if first:  # get into the ready pose once the controller is up
            self.cmd = list(self.joints)
            self.look_at(0.0, self.look[WRIST], 3.0)

    def on_command(self, msg: String):
        if self.cmd is None:
            return
        cmd = msg.data.strip().lower()
        if cmd == "record":
            self.start_recording()
            return
        if cmd == "release":
            self.release()
            return
        if self.state == "record":
            self.get_logger().info(f'ignoring "{cmd}": locked for recording, say "release" first')
            return
        if cmd == "hi":
            self.wave()
        elif cmd == "dumme":
            self.track_until = self.now() + self.track_time
            if self.state == "wave":
                self.after_wave = "track"
            elif self.person_visible():
                self.set_state("track")
            else:
                self.start_search()

    def on_target(self, msg: PointStamped):
        self.target = (msg.point.x, msg.point.y)
        self.target_time = self.now()
        if self.state == "search":
            self.look_at(self.joints[PAN], self.cmd[WRIST], 0.3)  # stop where it is
            self.set_state("track")
        if self.state != "track" or self.cmd is None:
            return
        x, y = self.target
        if abs(x) < self.deadband and abs(y) < self.deadband:
            return
        # person right of centre (x > 0) -> pan +; above centre (y < 0) -> wrist +
        self.look_at(self.cmd[PAN] + self.gain * x, self.cmd[WRIST] - self.gain * y, 0.25)

    # ------------------------------------------------------------- behaviours
    def start_recording(self):
        if self.state == "record":
            return
        # Lock exactly where the arm is now (also cuts a wave or search short).
        self.send([(list(self.joints), 0.3)])
        self.track_until = 0.0
        self.set_state("record")
        self.call_recorder(True)

    def release(self):
        if self.state != "record":
            return
        self.call_recorder(False)
        self.set_state("idle")

    def call_recorder(self, on):
        if not self.recorder.service_is_ready():
            self.get_logger().warn("video_recorder is not running: arm is locked but nothing is recorded")
            return
        future = self.recorder.call_async(SetBool.Request(data=on))

        def done(f):
            res = f.result()
            verb = "recording to" if on else "saved"
            if res is not None and res.success:
                self.get_logger().info(f"{verb} {res.message}")
            else:
                self.get_logger().warn(f"recorder: {res.message if res else 'no response'}")

        future.add_done_callback(done)

    def start_search(self):
        self.sweep_dir = 1.0 if self.cmd[PAN] <= 0 else -1.0  # head for the far side first
        self.sweep_turns = 0
        self.look_at(self.cmd[PAN], self.look[WRIST], 0.5)
        self.set_state("search")

    def wave(self):
        face = self.cmd[PAN]
        if self.person_visible():
            face += self.target[0]
        face = clamp(face, -self.pan_limit + self.wave_swing[0], self.pan_limit - self.wave_swing[0])
        base = list(self.look)
        base[PAN] = face
        points = [(base, 1.0)]
        half = self.wave_period / 2
        for i in range(2 * self.wave_count):
            s = 1 if i % 2 == 0 else -1
            pose = list(base)
            pose[PAN] += s * self.wave_swing[0]
            pose[ELBOW] += s * self.wave_swing[1]
            points.append((pose, half))
        points.append((base, half))
        t = self.send(points)
        self.after_wave = "track" if self.now() < self.track_until else "idle"
        self.wave_end = self.now() + t
        self.set_state("wave")

    def tick(self):
        if self.cmd is None:
            return
        now = self.now()
        if self.state == "wave":
            if now >= self.wave_end:
                self.set_state(self.after_wave)
        elif self.state == "track":
            if now > self.track_until:
                self.set_state("idle")
            elif now - self.target_time > self.lost_timeout:
                self.get_logger().info("lost you, searching")
                self.start_search()
        elif self.state == "search":
            if now > self.track_until:
                self.get_logger().info("could not find anyone")
                self.look_at(0.0, self.look[WRIST], 2.0)
                self.set_state("idle")
                return
            pan = self.cmd[PAN] + self.sweep_dir * self.search_speed * 0.1
            if abs(pan) >= self.pan_limit:
                self.sweep_dir = -self.sweep_dir
                self.sweep_turns += 1
                if self.sweep_turns > 2:
                    self.get_logger().info("searched everywhere, nobody here")
                    self.track_until = now
                    return
            self.look_at(pan, self.look[WRIST], 0.15)
        self.state_pub.publish(String(data=self.state))


def main():
    rclpy.init()
    node = Behavior()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
