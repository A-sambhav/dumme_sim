#!/usr/bin/env python3
"""Convert the Hugging Face 'Javiai/failures-3D-print' parquet into YOLO format.

Input : data/raw/train.parquet  (download link in README.md)
Output: data/yolo/{images,labels}/{train,val}/ + data/yolo/dataset.yaml

The dataset stores boxes as [x_center, y_center, width, height] in pixels;
YOLO wants the same layout normalised to 0-1 by image size.
"""
import argparse
import io
import random
from pathlib import Path

import pyarrow.parquet as pq
from PIL import Image

CLASSES = ["error", "extruder", "part", "spaghetti"]

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parquet", type=Path, default=HERE / "data/raw/train.parquet")
    ap.add_argument("--out", type=Path, default=HERE / "data/yolo")
    ap.add_argument("--val-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rows = pq.read_table(args.parquet).to_pylist()
    random.Random(args.seed).shuffle(rows)
    n_val = max(1, round(len(rows) * args.val_frac))

    counts = {"train": 0, "val": 0}
    for i, row in enumerate(rows):
        split = "val" if i < n_val else "train"
        img = Image.open(io.BytesIO(row["image"]["bytes"])).convert("RGB")
        w, h = img.size

        img_dir = args.out / "images" / split
        lbl_dir = args.out / "labels" / split
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)

        stem = f"{i:05d}"  # image_id is 52 for every row, so use the row index
        img.save(img_dir / f"{stem}.jpg", quality=95)

        lines = []
        for (xc, yc, bw, bh), cls in zip(row["objects"]["bbox"], row["objects"]["categories"]):
            xc, yc = min(max(xc / w, 0.0), 1.0), min(max(yc / h, 0.0), 1.0)
            bw, bh = min(bw / w, 1.0), min(bh / h, 1.0)
            if bw > 0 and bh > 0:
                lines.append(f"{cls} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")
        (lbl_dir / f"{stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""))
        counts[split] += 1

    yaml = args.out / "dataset.yaml"
    yaml.write_text(
        f"path: {args.out.resolve()}\n"
        "train: images/train\n"
        "val: images/val\n"
        "names:\n" + "".join(f"  {i}: {c}\n" for i, c in enumerate(CLASSES))
    )
    print(f"train={counts['train']} val={counts['val']} -> {yaml}")


if __name__ == "__main__":
    main()
