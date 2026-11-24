#!/usr/bin/env python3
import rclpy
import numpy as np
from rclpy.node import Node
from rclpy.action import ActionServer
from dumme_msgs.action import DummeTask
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState


class TaskServer(Node):
    def __init__(self):
        super().__init__("task_server")
        self.get_logger().info("Starting the Server")
        self.action_server = ActionServer(
            self, DummeTask, "task_server", self.goalCallback
        )

        # MoveIt 2 Interface
        self.dumme = MoveItPy(node_name="moveit_py")
        self.dumme_arm = self.dumme.get_planning_component("arm")

    def goalCallback(self, goal_handle):
        self.get_logger().info(
            "Received goal request with id %d" % goal_handle.request.task_number
        )

        arm_state = RobotState(self.dumme.get_robot_model())

        # Joint order: shoulder_rotation_plate_joint, shoulder_joint, elbow_joint, wrist_joint
        if goal_handle.request.task_number == 0:
            arm_joint_goal = np.array([0.0, 0.0, 0.0, 0.0])
        elif goal_handle.request.task_number == 1:
            arm_joint_goal = np.array([-1.14, -0.6, -0.07, 0.0])
        elif goal_handle.request.task_number == 2:
            arm_joint_goal = np.array([-1.57, 0.0, -0.9, 0.0])
        else:
            self.get_logger().error("Invalid Task Number")
            return

        arm_state.set_joint_group_positions("arm", arm_joint_goal)

        self.dumme_arm.set_start_state_to_current_state()
        self.dumme_arm.set_goal_state(robot_state=arm_state)

        arm_plan_result = self.dumme_arm.plan()

        if arm_plan_result:
            self.get_logger().info("Planner SUCCEED, moving the arm")
            self.dumme.execute(arm_plan_result.trajectory, controllers=[])
        else:
            self.get_logger().info("Planner failed!")

        self.get_logger().info("Goal succeeded")
        goal_handle.succeed()
        result = DummeTask.Result()
        result.success = True
        return result


def main(args=None):
    rclpy.init(args=args)
    task_server = TaskServer()
    rclpy.spin(task_server)


if __name__ == "__main__":
    main()
