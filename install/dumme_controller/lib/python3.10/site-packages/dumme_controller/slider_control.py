#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class SliderControl(Node):
    """
    Bridges joint_state_publisher_gui sliders (published on /joint_commands)
    into a JointTrajectory goal for arm_controller, so Dumme's joints can be
    jogged by hand in RViz/Gazebo without MoveIt.
    """

    ARM_JOINTS = [
        "shoulder_rotation_plate_joint",
        "shoulder_joint",
        "elbow_joint",
        "wrist_joint",
    ]

    def __init__(self):
        super().__init__("slider_control")
        self.arm_pub_ = self.create_publisher(
            JointTrajectory, "arm_controller/joint_trajectory", 10
        )
        self.sub_ = self.create_subscription(
            JointState, "joint_commands", self.slider_callback, 10
        )
        self.get_logger().info("Slider Control Node started")

    def slider_callback(self, msg):
        name_to_position = dict(zip(msg.name, msg.position))
        try:
            positions = [name_to_position[j] for j in self.ARM_JOINTS]
        except KeyError as missing_joint:
            self.get_logger().warn(
                f"Waiting on joint {missing_joint} from /joint_commands"
            )
            return

        arm_trajectory = JointTrajectory()
        arm_trajectory.joint_names = self.ARM_JOINTS

        goal_point = JointTrajectoryPoint()
        goal_point.positions = positions

        arm_trajectory.points.append(goal_point)
        self.arm_pub_.publish(arm_trajectory)


def main():
    rclpy.init()

    node = SliderControl()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()