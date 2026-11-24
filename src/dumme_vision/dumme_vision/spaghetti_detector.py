#!/usr/bin/env python3
"""Detect 3D-print spaghetti failures in a camera stream with YOLOv8n.

Subscribes:
  image_topic (sensor_msgs/Image)       camera frames, default /camera/image_raw

Publishes (under ~/), in the upright (rotated by image_rotation) image frame:
  detections  (vision_msgs/Detection2DArray)  every box above `conf`, every processed frame
  detected    (std_msgs/Bool)                 debounced alarm: True once an alert class is
                                              seen in >= min_hits of the last `window` frames
  image_annotated (sensor_msgs/Image)         frame with boxes drawn (if publish_annotated)

Needs ultralytics, so run it with the workspace venv's python (the launch
file does this). Only the newest frame is processed, at most `rate_hz` times
a second, so a slow CPU never builds up a backlog.
"""
from collections import deque

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from ultralytics import YOLO

from dumme_vision.image_utils import bgr_to_image, image_to_bgr, rotate_cw


class SpaghettiDetector(Node):
    def __init__(self):
        super().__init__("spaghetti_detector")

        self.declare_parameter("model_path", "")
        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("rate_hz", 2.0)
        self.declare_parameter("conf", 0.4)
        self.declare_parameter("imgsz", 640)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("alert_classes", ["spaghetti"])
        self.declare_parameter("window", 5)
        self.declare_parameter("min_hits", 3)
        self.declare_parameter("publish_annotated", True)
        self.declare_parameter("image_rotation", 0)  # clockwise degrees applied before inference

        p = lambda n: self.get_parameter(n).value  # noqa: E731
        model_path = p("model_path")
        if not model_path:
            raise RuntimeError("parameter 'model_path' is required")
        self.conf = float(p("conf"))
        self.imgsz = int(p("imgsz"))
        self.device = p("device")
        self.alert_classes = set(p("alert_classes"))
        self.min_hits = int(p("min_hits"))
        self.history = deque(maxlen=int(p("window")))
        self.publish_annotated = bool(p("publish_annotated"))
        self.rotation = int(p("image_rotation"))
        rotate_cw(np.zeros((2, 2, 3)), self.rotation)  # validate early

        self.get_logger().info(f"Loading model {model_path}")
        self.model = YOLO(model_path)
        unknown = self.alert_classes - set(self.model.names.values())
        if unknown:
            self.get_logger().warn(f"alert_classes not in model: {sorted(unknown)}")

        self.latest = None
        self.alarm = False

        self.create_subscription(Image, p("image_topic"), self.on_image, qos_profile_sensor_data)
        self.det_pub = self.create_publisher(Detection2DArray, "~/detections", 10)
        self.flag_pub = self.create_publisher(Bool, "~/detected", 10)
        self.img_pub = self.create_publisher(Image, "~/image_annotated", 1)
        self.create_timer(1.0 / float(p("rate_hz")), self.process)

        self.get_logger().info(
            f"Watching {p('image_topic')} at {p('rate_hz')} Hz, alert on "
            f"{sorted(self.alert_classes)} in {self.min_hits}/{self.history.maxlen} frames"
        )

    def on_image(self, msg: Image):
        self.latest = msg

    def process(self):
        msg, self.latest = self.latest, None
        if msg is None:
            return
        try:
            frame = rotate_cw(image_to_bgr(msg), self.rotation)
        except ValueError as e:
            self.get_logger().error(str(e), throttle_duration_sec=5.0)
            return

        result = self.model.predict(
            frame, conf=self.conf, imgsz=self.imgsz, device=self.device, verbose=False
        )[0]

        out = Detection2DArray(header=msg.header)
        hit = False
        for xywh, cls, score in zip(
            result.boxes.xywh.tolist(), result.boxes.cls.tolist(), result.boxes.conf.tolist()
        ):
            name = self.model.names[int(cls)]
            hit |= name in self.alert_classes
            det = Detection2D(header=msg.header)
            det.bbox.center.position.x, det.bbox.center.position.y = xywh[0], xywh[1]
            det.bbox.size_x, det.bbox.size_y = xywh[2], xywh[3]
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = name
            hyp.hypothesis.score = float(score)
            det.results.append(hyp)
            out.detections.append(det)
        self.det_pub.publish(out)

        self.history.append(hit)
        alarm = sum(self.history) >= self.min_hits
        if alarm != self.alarm:
            if alarm:
                self.get_logger().warn("SPAGHETTI DETECTED - print is failing")
            else:
                self.get_logger().info("Spaghetti alarm cleared")
            self.alarm = alarm
        self.flag_pub.publish(Bool(data=alarm))

        if self.publish_annotated and self.img_pub.get_subscription_count() > 0:
            self.img_pub.publish(bgr_to_image(result.plot(), msg.header))


def main():
    rclpy.init()
    node = SpaghettiDetector()
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
