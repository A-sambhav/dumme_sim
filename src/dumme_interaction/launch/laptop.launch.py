"""Real robot, laptop side: everything except the arm controller.

  Pi:      ros2 launch dumme_controller pi.launch.py
  Laptop:  ros2 launch dumme_interaction laptop.launch.py
           ros2 launch dumme_interaction laptop.launch.py rviz:=True voice:=False

Starts the person detector, video recorder, voice listener and behaviour node
(interaction.launch.py). The behaviour node reads /joint_states from the Pi
and sends trajectories to /arm_controller/joint_trajectory over Wi-Fi, so the
Pi and laptop must share ROS_DOMAIN_ID. The camera must publish on
/camera/image_raw.
"""
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    args = [
        DeclareLaunchArgument("voice", default_value="True",
                              description="Listen on the microphone"),
        DeclareLaunchArgument("mic_device", default_value="default",
                              description="arecord -D device, see `arecord -L`"),
        DeclareLaunchArgument("record_fps", default_value="15.0",
                              description="Camera frame rate, so recordings play at the right speed"),
        DeclareLaunchArgument("rviz", default_value="False",
                              description="Show the arm in RViz (robot model from the Pi)"),
    ]

    interaction = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("dumme_interaction"), "launch",
                         "interaction.launch.py")
        ),
        launch_arguments={
            "use_sim_time": "False",
            "voice": LaunchConfiguration("voice"),
            "mic_device": LaunchConfiguration("mic_device"),
            "record_fps": LaunchConfiguration("record_fps"),
        }.items(),
    )

    # robot_state_publisher runs on the Pi; add a RobotModel display on the
    # /robot_description topic and set the fixed frame to "world".
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        condition=IfCondition(LaunchConfiguration("rviz")),
    )

    return LaunchDescription(args + [interaction, rviz])
