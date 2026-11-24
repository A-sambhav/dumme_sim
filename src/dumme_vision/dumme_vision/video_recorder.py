#!/usr/bin/env python3
"""Record the camera stream to MP4 files on demand.

Service:
  ~/record (std_srvs/SetBool)   true = start a new file, false = stop and close it;
                                the response message is the file path
Subscribes:
  image_topic (sensor_msgs/Image)  default /camera/image_raw

Files go to `output_dir` as dumme_YYYYmmdd_HHMMSS.mp4, rotated upright by
`image_rotation` (Dumm-E's wrist camera is mounted on its side). Frames are
written as they arrive; `fps` should match the camera rate so playback speed
is right (Gazebo camera: 15 Hz).
"""
import os
import time

import cv2
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_srvs.srv import SetBool

from dumme_vision.image_utils import image_to_bgr, rotate_cw


class VideoRecorder(Node):
    def __init__(self):
        super().__init__("video_recorder")
        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("output_dir", os.path.expanduser("~/dumme_recordings"))
        self.declare_parameter("fps", 15.0)
        self.declare_parameter("image_rotation", 0)

        p = lambda n: self.get_parameter(n).value  # noqa: E731
        self.output_dir = os.path.expanduser(p("output_dir"))
        self.fps = float(p("fps"))
        self.rotation = int(p("image_rotation"))

        self.writer = None
        self.path = None
        self.frames = 0
        self.started = 0.0

        self.create_subscription(Image, p("image_topic"), self.on_image, qos_profile_sensor_data)
        self.create_service(SetBool, "~/record", self.on_record)
        self.get_logger().info(f"Ready to record {p('image_topic')} into {self.output_dir}")

    def on_record(self, req, res):
        if req.data:
            if self.writer is not None or self.path is not None:
                res.success, res.message = True, self.path  # already recording
                return res
            os.makedirs(self.output_dir, exist_ok=True)
            self.path = os.path.join(self.output_dir, time.strftime("dumme_%Y%m%d_%H%M%S.mp4"))
            self.frames, self.started = 0, time.monotonic()
            self.get_logger().info(f"Recording to {self.path}")
            res.success, res.message = True, self.path
        else:
            res.success, res.message = self.stop()
        return res

    def stop(self):
        if self.path is None:
            return False, "not recording"
        path, frames = self.path, self.frames
        if self.writer is not None:
            self.writer.release()
        self.writer, self.path = None, None
        secs = time.monotonic() - self.started
        if frames == 0:
            self.get_logger().warn("Stopped recording, but no frames arrived (camera running?)")
            return False, "no frames received"
        self.get_logger().info(f"Saved {path} ({frames} frames, {secs:.1f} s)")
        return True, path

    def on_image(self, msg: Image):
        if self.path is None:
            return
        try:
            frame = rotate_cw(image_to_bgr(msg), self.rotation)
        except ValueError as e:
            self.get_logger().error(str(e), throttle_duration_sec=5.0)
            return
        if self.writer is None:  # open lazily: frame size is only known now
            h, w = frame.shape[:2]
            self.writer = cv2.VideoWriter(self.path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (w, h))
        self.writer.write(frame)
        self.frames += 1

    def destroy_node(self):
        if self.path is not None:
            self.stop()
        super().destroy_node()


def main():
    rclpy.init()
    node = VideoRecorder()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
