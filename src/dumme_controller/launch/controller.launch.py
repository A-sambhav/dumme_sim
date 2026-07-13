import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    is_sim = LaunchConfiguration("is_sim")

    is_sim_arg = DeclareLaunchArgument(
        name="is_sim",
        default_value="True",
        description="Set to false when running on real hardware",
    )

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("dumme_description"),
                    "urdf",
                    "dumme_description.urdf.xacro",
                ),
                " is_sim:=False",
            ]
        ),
        value_type=str,
    )

    # When is_sim is True, Gazebo's own ros2_control plugin already starts
    # robot_state_publisher's data via the spawned robot_description topic
    # and brings up the controller_manager itself, so these two nodes are
    # only needed for the real robot.
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": False,
            }
        ],
        condition=UnlessCondition(is_sim),
    )

    controller_manager_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {
                "robot_description": robot_description,
                "use_sim_time": is_sim,
            },
            os.path.join(
                get_package_share_directory("dumme_controller"),
                "config",
                "dumme_controllers.yaml",
            ),
        ],
        condition=UnlessCondition(is_sim),
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    return LaunchDescription(
        [
            is_sim_arg,
            robot_state_publisher_node,
            controller_manager_node,
            joint_state_broadcaster_spawner,
            arm_controller_spawner,
        ]
    )