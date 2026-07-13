import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node


def generate_launch_description():

    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("dumme_controller"),
                "launch",
                "controller.launch.py",
            )
        ),
        launch_arguments={"is_sim": "True"}.items(),
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        remappings=[
            ("/joint_states", "/joint_commands"),
        ],
    )

    slider_control_node = Node(
        package="dumme_controller",
        executable="slider_control",
    )

    return LaunchDescription(
        [
            controller,
            joint_state_publisher_gui_node,
            slider_control_node,
        ]
    )