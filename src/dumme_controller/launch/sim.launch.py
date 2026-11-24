import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    """Gazebo + controllers + joint sliders + wrist camera feed, in one go."""

    camera_view = LaunchConfiguration("camera_view")

    camera_view_arg = DeclareLaunchArgument(
        name="camera_view",
        default_value="True",
        description="Open rqt_image_view on the wrist camera feed",
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("dumme_description"),
                "launch",
                "gazebo.launch.py",
            )
        )
    )

    # Controller spawners need Gazebo's controller_manager to be up first.
    slider_controller = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("dumme_controller"),
                        "launch",
                        "slider_controller.launch.py",
                    )
                )
            )
        ],
    )

    camera_viewer = Node(
        package="rqt_image_view",
        executable="rqt_image_view",
        arguments=["/camera/image_raw"],
        parameters=[{"use_sim_time": True}],
        condition=IfCondition(camera_view),
    )

    return LaunchDescription(
        [
            camera_view_arg,
            gazebo,
            slider_controller,
            camera_viewer,
        ]
    )
