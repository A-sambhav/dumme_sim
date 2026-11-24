"""Real robot, Raspberry Pi Zero 2 W side: just the arm controller.

  ros2 launch dumme_controller pi.launch.py                    # ESP32 on /dev/ttyUSB0
  ros2 launch dumme_controller pi.launch.py port:=/dev/ttyACM0

Runs robot_state_publisher, controller_manager with DummeInterface (talks to
the ESP32 over USB serial, 115200), joint_state_broadcaster and arm_controller.
Everything heavy (person/spaghetti detection, voice, recording, behaviours)
runs on the laptop with `ros2 launch dumme_interaction laptop.launch.py`;
the two find each other over Wi-Fi, so both need the same ROS_DOMAIN_ID.

On the Pi only these packages are needed:
  colcon build --packages-select dumme_description dumme_controller
"""
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    port_arg = DeclareLaunchArgument(
        name="port",
        default_value="/dev/ttyUSB0",
        description="ESP32 serial port, see `ls /dev/ttyUSB* /dev/ttyACM*`",
    )

    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("dumme_controller"),
                "launch",
                "controller.launch.py",
            )
        ),
        launch_arguments={
            "is_sim": "False",
            "port": LaunchConfiguration("port"),
        }.items(),
    )

    return LaunchDescription([port_arg, controller])
