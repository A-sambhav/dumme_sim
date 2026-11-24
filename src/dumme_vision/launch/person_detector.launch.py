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
            default_value=str(ws / "ml" / "models" / "yolov8n.pt"),
            description="COCO-pretrained YOLOv8n (downloaded automatically if missing)",
        ),
        DeclareLaunchArgument("image_topic", default_value="/camera/image_raw"),
        DeclareLaunchArgument("rate_hz", default_value="5.0"),
        DeclareLaunchArgument("conf", default_value="0.5"),
        DeclareLaunchArgument("image_rotation", default_value="90"),
        DeclareLaunchArgument("use_sim_time", default_value="False"),
    ]

    detector = Node(
        package="dumme_vision",
        executable="person_detector.py",
        prefix=LaunchConfiguration("python"),
        output="screen",
        parameters=[
            {
                "model_path": LaunchConfiguration("model_path"),
                "image_topic": LaunchConfiguration("image_topic"),
                "rate_hz": LaunchConfiguration("rate_hz"),
                "conf": LaunchConfiguration("conf"),
                "image_rotation": LaunchConfiguration("image_rotation"),
                "use_sim_time": LaunchConfiguration("use_sim_time"),
            }
        ],
    )

    return LaunchDescription(args + [detector])
