#!/usr/bin/env python3
"""Detect people in the camera stream with a COCO-pretrained YOLOv8n.

Subscribes:
  image_topic (sensor_msgs/Image)          camera frames, default /camera/image_raw

Publishes (under ~/), in the upright image frame (raw frame rotated by image_rotation):
  detections      (vision_msgs/Detection2DArray)  every person box above `conf`
  target          (geometry_msgs/PointStamped)    the biggest (= closest) person, only
                                                  when someone is visible:
                                                    x = horizontal angle from centre, rad, + right
                                                    y = vertical angle from centre,  rad, + down,
                                                        aimed at the face (top 15% of the box)
                                                    z = box height / image height
  image_annotated (sensor_msgs/Image)             frame with boxes (only if subscribed)

Angles use a pinhole model from `hfov`, the RAW camera's horizontal field of
view (the Gazebo camera and ESP32-CAM OV2640 are both ~1.15 rad).
"""
import math

import numpy as np
import rclpy
from geometry_msgs.msg import PointStamped
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose
from ultralytics import YOLO

from dumme_vision.image_utils import bgr_to_image, image_to_bgr, rotate_cw

PERSON = 0  # COCO class id
FACE = 0.15  # look-at point: this far down from the top of the person box


class PersonDetector(Node):
    def __init__(self):
        super().__init__("person_detector")
        self.declare_parameter("model_path", "")
        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("rate_hz", 5.0)
        self.declare_parameter("conf", 0.5)
        self.declare_parameter("imgsz", 320)
        self.declare_parameter("device", "cpu")
        self.declare_parameter("image_rotation", 0)
        self.declare_parameter("hfov", 1.15)

        p = lambda n: self.get_parameter(n).value  # noqa: E731
        if not p("model_path"):
            raise RuntimeError("parameter 'model_path' is required")
        self.conf = float(p("conf"))
        self.imgsz = int(p("imgsz"))
        self.device = p("device")
        self.rotation = int(p("image_rotation"))
        rotate_cw(np.zeros((2, 2, 3)), self.rotation)  # validate early
        self.hfov = float(p("hfov"))

        self.get_logger().info(f"Loading model {p('model_path')}")
        self.model = YOLO(p("model_path"))
        self.latest = None

        self.create_subscription(Image, p("image_topic"), self.on_image, qos_profile_sensor_data)
        self.det_pub = self.create_publisher(Detection2DArray, "~/detections", 10)
        self.target_pub = self.create_publisher(PointStamped, "~/target", 10)
        self.img_pub = self.create_publisher(Image, "~/image_annotated", 1)
        self.create_timer(1.0 / float(p("rate_hz")), self.process)
        self.get_logger().info(f"Watching {p('image_topic')} for people at {p('rate_hz')} Hz")

    def on_image(self, msg: Image):
        self.latest = msg

    def process(self):
        msg, self.latest = self.latest, None
        if msg is None:
            return
        try:
            raw = image_to_bgr(msg)
        except ValueError as e:
            self.get_logger().error(str(e), throttle_duration_sec=5.0)
            return
        focal = (raw.shape[1] / 2) / math.tan(self.hfov / 2)
        frame = rotate_cw(raw, self.rotation)
        h, w = frame.shape[:2]

        result = self.model.predict(
            frame, conf=self.conf, imgsz=self.imgsz, device=self.device,
            classes=[PERSON], verbose=False,
        )[0]

        out = Detection2DArray(header=msg.header)
        best = None
        for xywh, score in zip(result.boxes.xywh.tolist(), result.boxes.conf.tolist()):
            det = Detection2D(header=msg.header)
            det.bbox.center.position.x, det.bbox.center.position.y = xywh[0], xywh[1]
            det.bbox.size_x, det.bbox.size_y = xywh[2], xywh[3]
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = "person"
            hyp.hypothesis.score = float(score)
            det.results.append(hyp)
            out.detections.append(det)
            if best is None or xywh[3] > best[3]:
                best = xywh
        self.det_pub.publish(out)

        if best is not None:
            t = PointStamped(header=msg.header)
            t.point.x = math.atan2(best[0] - w / 2, focal)
            face_y = best[1] - best[3] * (0.5 - FACE)
            t.point.y = math.atan2(face_y - h / 2, focal)
            t.point.z = best[3] / h
            self.target_pub.publish(t)

        if self.img_pub.get_subscription_count() > 0:
            self.img_pub.publish(bgr_to_image(result.plot(), msg.header))


def main():
    rclpy.init()
    node = PersonDetector()
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
