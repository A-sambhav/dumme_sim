# Spaghetti detector (YOLOv8n)

Detects 3D-print failures in camera images. Classes: `error`, `extruder`,
`part`, `spaghetti`. Trained model: `models/spaghetti_yolov8n.pt` (~6 MB,
~26 ms per image on this machine's CPU).

## Setup (once)
```bash
cd ml
python3 -m venv .venv
.venv/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install ultralytics pyarrow
```
Run the scripts with `env -u PYTHONPATH` so ROS's Python path doesn't leak
into the venv.

## Data
[Javiai/failures-3D-print](https://huggingface.co/datasets/Javiai/failures-3D-print)
on Hugging Face: 73 images, 192 boxes, licence not stated.
```bash
cd ml/spaghetti
mkdir -p data/raw
curl -L -o data/raw/train.parquet \
  https://huggingface.co/datasets/Javiai/failures-3D-print/resolve/main/data/train-00000-of-00001-d89ab36ef5b3866d.parquet
env -u PYTHONPATH ../.venv/bin/python prepare_dataset.py   # -> data/yolo/ (58 train / 15 val)
```

## Train
```bash
env -u PYTHONPATH ../.venv/bin/python train.py            # ~16 min on CPU, 100 epochs
```
Any YOLO-format dataset works: `train.py --data path/to/dataset.yaml`.

## Try it
```bash
env -u PYTHONPATH ../.venv/bin/yolo predict model=models/spaghetti_yolov8n.pt source=some_image.jpg conf=0.35
```

## Current results (15 validation images)
| class | AP50 |
|---|---|
| spaghetti | 0.717 |
| part | 0.851 |
| extruder | 0.835 |
| error | 0.555 |
| **all** | **0.739** |

With only 15 validation images, these numbers are rough estimates. Some
validation images are frames from the same videos as training images, so real
accuracy on your printer will be lower. To improve it, add frames from the
ESP32-CAM pointed at your own printer, both good prints and failures.
