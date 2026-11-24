from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # <ws>/install/dumme_vision/share/dumme_vision -> <ws>
    ws = Path(get_package_share_directory("dumme_vision")).parents[3]

    args = [
        DeclareLaunchArgument(
            "python",
            default_value=str(ws / "ml" / ".venv" / "bin" / "python"),
            description="Python with ultralytics installed (see ml/spaghetti/README.md)",
        ),
        DeclareLaunchArgument(
            "model_path",
            default_value=str(ws / "ml" / "spaghetti" / "models" / "spaghetti_yolov8n.pt"),
        ),
        DeclareLaunchArgument("image_topic", default_value="/camera/image_raw"),
        DeclareLaunchArgument("rate_hz", default_value="2.0"),
        DeclareLaunchArgument("conf", default_value="0.4"),
        DeclareLaunchArgument("use_sim_time", default_value="False"),
        # Dumm-E's wrist camera is mounted on its side: 90 deg clockwise makes frames upright
        DeclareLaunchArgument("image_rotation", default_value="90"),
    ]

    detector = Node(
        package="dumme_vision",
        executable="spaghetti_detector.py",
        prefix=LaunchConfiguration("python"),
        output="screen",
        parameters=[
            {
                "model_path": LaunchConfiguration("model_path"),
                "image_topic": LaunchConfiguration("image_topic"),
                "rate_hz": LaunchConfiguration("rate_hz"),
                "conf": LaunchConfiguration("conf"),
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                "image_rotation": LaunchConfiguration("image_rotation"),
            }
        ],
    )

    return LaunchDescription(args + [detector])
