"""Person detector + video recorder + voice keywords + behaviour node.

  ros2 launch dumme_interaction interaction.launch.py            # real robot
  ros2 launch dumme_controller sim.launch.py interaction:=True   # in Gazebo

Joint sliders must NOT run at the same time: they stream positions that
override the behaviour node.
"""
import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # <ws>/install/dumme_interaction/share/dumme_interaction -> <ws>
    ws = Path(get_package_share_directory("dumme_interaction")).parents[3]
    use_sim_time = LaunchConfiguration("use_sim_time")

    args = [
        DeclareLaunchArgument("use_sim_time", default_value="False"),
        DeclareLaunchArgument("voice", default_value="True",
                              description="Listen on the microphone (False: only /voice/command)"),
        DeclareLaunchArgument("mic_device", default_value="default",
                              description="arecord -D device, see `arecord -L`"),
        DeclareLaunchArgument(
            "python", default_value=str(ws / "ml" / ".venv" / "bin" / "python"),
            description="Python with ultralytics + vosk installed",
        ),
        DeclareLaunchArgument(
            "recordings_dir", default_value=os.path.expanduser("~/dumme_recordings"),
            description='Where "start recording" saves MP4s',
        ),
        DeclareLaunchArgument("record_fps", default_value="15.0",
                              description="Camera frame rate (Gazebo camera: 15)"),
        DeclareLaunchArgument(
            "vosk_model",
            default_value=str(ws / "ml" / "voice" / "models" / "vosk-model-small-en-us-0.15"),
        ),
    ]

    person_detector = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("dumme_vision"), "launch",
                         "person_detector.launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "python": LaunchConfiguration("python"),
        }.items(),
    )

    voice = Node(
        package="dumme_interaction",
        executable="voice_listener.py",
        prefix=LaunchConfiguration("python"),
        output="screen",
        parameters=[{
            "model_path": LaunchConfiguration("vosk_model"),
            "device": LaunchConfiguration("mic_device"),
        }],
        condition=IfCondition(LaunchConfiguration("voice")),
    )

    recorder = Node(
        package="dumme_vision",
        executable="video_recorder.py",
        prefix=LaunchConfiguration("python"),  # needs OpenCV from the venv
        output="screen",
        parameters=[{
            "output_dir": LaunchConfiguration("recordings_dir"),
            "fps": LaunchConfiguration("record_fps"),
            "image_rotation": 90,  # wrist camera is mounted on its side
            "use_sim_time": use_sim_time,
        }],
    )

    behavior = Node(
        package="dumme_interaction",
        executable="behavior.py",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
    )

    return LaunchDescription(args + [person_detector, recorder, voice, behavior])
