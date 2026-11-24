#!/usr/bin/env python3
"""Fine-tune YOLOv8n on the spaghetti dataset (CPU by default).

Run prepare_dataset.py first. Best weights land in
runs/<name>/weights/best.pt; a copy is placed at models/spaghetti_yolov8n.pt.
"""
import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", type=Path, default=HERE / "data/yolo/dataset.yaml")
    ap.add_argument("--model", default="yolov8n.pt", help="starting weights (COCO-pretrained)")
    ap.add_argument("--epochs", type=int, default=100)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--name", default="spaghetti")
    args = ap.parse_args()

    model = YOLO(args.model)
    model.train(
        data=str(args.data),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=str(HERE / "runs"),
        name=args.name,
        exist_ok=True,
        patience=30,      # stop early if val mAP stalls
        workers=8,
        seed=0,
        plots=True,
    )

    best = HERE / "runs" / args.name / "weights" / "best.pt"
    out = HERE / "models" / "spaghetti_yolov8n.pt"
    out.parent.mkdir(exist_ok=True)
    shutil.copy(best, out)

    metrics = YOLO(str(out)).val(data=str(args.data), device=args.device, plots=False)
    print(f"\nmAP50={metrics.box.map50:.3f}  mAP50-95={metrics.box.map:.3f}")
    for j, cls in enumerate(metrics.box.ap_class_index):
        print(f"  {metrics.names[int(cls)]:10s} AP50={metrics.box.ap50[j]:.3f}")
    print(f"model -> {out}")


if __name__ == "__main__":
    main()
