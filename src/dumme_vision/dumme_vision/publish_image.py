#!/usr/bin/env python3
"""Publish image file(s) on a topic in a loop - for testing the detector
without a camera.

  ros2 run dumme_vision publish_image.py --ros-args -p files:="['a.jpg','b.jpg']" -p topic:=/camera/image_raw
"""
import numpy as np
import rclpy
from PIL import Image as PILImage
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image


class ImagePublisher(Node):
    def __init__(self):
        super().__init__("image_file_publisher")
        self.declare_parameter("files", [""])
        self.declare_parameter("topic", "/camera/image_raw")
        self.declare_parameter("rate_hz", 5.0)
        self.declare_parameter("frame_id", "rgb_camera")
        files = [f for f in self.get_parameter("files").value if f]
        if not files:
            raise RuntimeError("parameter 'files' is required")
        self.frames = [np.asarray(PILImage.open(f).convert("RGB")) for f in files]
        self.frame_id = self.get_parameter("frame_id").value
        self.i = 0
        self.pub = self.create_publisher(
            Image, self.get_parameter("topic").value, qos_profile_sensor_data
        )
        self.create_timer(1.0 / self.get_parameter("rate_hz").value, self.tick)
        self.get_logger().info(f"Publishing {len(files)} image(s) on {self.pub.topic_name}")

    def tick(self):
        img = self.frames[self.i % len(self.frames)]
        self.i += 1
        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id
        msg.height, msg.width = img.shape[:2]
        msg.encoding = "rgb8"
        msg.step = msg.width * 3
        msg.data = img.tobytes()
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = ImagePublisher()
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
