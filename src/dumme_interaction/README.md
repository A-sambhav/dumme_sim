# dumme_interaction

Dumm-E's social behaviours, driven by voice and the wrist camera.

| You say | Dumm-E does |
|---|---|
| "hi" / "hello" / "hey" | turns to face you (if you are in view) and waves |
| "dummy" (Dumm-E) | looks at your face and follows you for 20 s; if you are not in view it sweeps its base around to find you |
| "(hey dummy) start recording" | locks the arm where it is and records the camera to `~/dumme_recordings/dumme_<date>_<time>.mp4`; ignores "hi"/"dummy" while locked |
| "release" (or "stop recording") | stops recording, saves the file, unlocks |

To film from a particular angle: say "dummy" so it looks at you (or move it there),
then "start recording" - it stays exactly there until "release".

## Run

```bash
# Gazebo: sliders are replaced by the behaviours, a person stands in the world
ros2 launch dumme_controller sim.launch.py interaction:=True

# real robot (controller already running)
ros2 launch dumme_interaction interaction.launch.py
```

Launch args: `voice:=False` (no microphone), `mic_device:=<arecord -L name>`,
`recordings_dir:=<dir>`, `record_fps:=<camera fps>`.
The joint sliders must not run at the same time: they stream positions that
override the behaviour node.

Without a microphone:

```bash
ros2 topic pub --once /voice/command std_msgs/msg/String "{data: dumme}"
ros2 topic pub --once /voice/command std_msgs/msg/String "{data: hi}"
ros2 topic pub --once /voice/command std_msgs/msg/String "{data: record}"
ros2 topic pub --once /voice/command std_msgs/msg/String "{data: release}"
```

In Gazebo, drag the person around (translate tool) to watch it follow / search.

## Nodes

- `voice_listener.py` (venv python): `arecord` -> Vosk small English model with a
  keyword-only grammar -> `/voice/command` (`hi` | `dumme` | `record` | `release`).
  Offline. Keywords need confidence >= `min_conf` (0.9), which rejects ordinary
  chatter. Recording phrases win, so "hey dummy start recording" doesn't also wave.
- `dumme_vision/person_detector.py` (venv python): COCO YOLOv8n, people only, 5 Hz ->
  `/person_detector/target` = angles of the closest person's face in the upright image.
- `dumme_vision/video_recorder.py` (venv python): `~/record` (std_srvs/SetBool) starts /
  stops an upright MP4 of the camera.
- `behavior.py`: state machine `idle | search | track | wave | record` -> `/arm_controller/joint_trajectory`.
  Pan = base joint, tilt = wrist joint, from `look_pose` (arm up, wrist folded so the
  camera faces forward). Every move is limited to `max_speed` (0.9 rad/s; the URDF
  limit is 1 rad/s, and Gazebo's position loop overshoots past it).

## Setup

```bash
cd ml && env -u PYTHONPATH .venv/bin/pip install vosk
mkdir -p voice/models && cd voice/models
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && unzip vosk-model-small-en-us-0.15.zip
```

`ml/models/yolov8n.pt` (COCO weights) is downloaded by ultralytics on first use.

## Notes

- The wrist camera is mounted on its side, so detectors rotate frames 90 deg
  clockwise (`image_rotation`) before inference; all image angles are upright.
- On the real arm the poses assume the servo zero offsets match the URDF; check
  `look_pose` before trusting it near the printer.
