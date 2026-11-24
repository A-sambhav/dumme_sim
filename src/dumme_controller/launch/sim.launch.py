import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    """Gazebo + controllers + joint sliders + wrist camera feed, in one go.

    interaction:=True swaps the joint sliders for Dumm-E's behaviours
    (person detector, "hi"/"dummy" voice commands, wave / look / search).
    """

    camera_view = LaunchConfiguration("camera_view")
    interaction = LaunchConfiguration("interaction")

    camera_view_arg = DeclareLaunchArgument(
        name="camera_view",
        default_value="True",
        description="Open rqt_image_view on the wrist camera feed",
    )

    interaction_arg = DeclareLaunchArgument(
        name="interaction",
        default_value="False",
        description="Run the interaction behaviours instead of the joint sliders",
    )

    voice_arg = DeclareLaunchArgument(
        name="voice",
        default_value="True",
        description="With interaction: listen on the microphone",
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
                ),
                condition=UnlessCondition(interaction),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("dumme_controller"),
                        "launch",
                        "controller.launch.py",
                    )
                ),
                launch_arguments={"is_sim": "True"}.items(),
                condition=IfCondition(interaction),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory("dumme_interaction"),
                        "launch",
                        "interaction.launch.py",
                    )
                ),
                launch_arguments={
                    "use_sim_time": "True",
                    "voice": LaunchConfiguration("voice"),
                }.items(),
                condition=IfCondition(interaction),
            ),
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
            interaction_arg,
            voice_arg,
            gazebo,
            slider_controller,
            camera_viewer,
        ]
    )
