# split_train_val.py
import os
import shutil
from pathlib import Path
import random

random.seed(42)

train_img_dir = Path('data/yolo/train/images')
train_lbl_dir = Path('data/yolo/train/labels')
val_img_dir   = Path('data/yolo/val/images')
val_lbl_dir   = Path('data/yolo/val/labels')

val_img_dir.mkdir(parents=True, exist_ok=True)
val_lbl_dir.mkdir(parents=True, exist_ok=True)

img_files = list(train_img_dir.glob('*.*'))
random.shuffle(img_files)

val_count = int(0.2 * len(img_files))  # 20% to val
val_files = img_files[:val_count]

print(f"Moving {val_count} images from train → val...")

for img_path in val_files:
    base = img_path.stem
    lbl_path = train_lbl_dir / f"{base}.txt"

    # Move image
    shutil.move(str(img_path), val_img_dir / img_path.name)
    # Move label
    if lbl_path.exists():
        shutil.move(str(lbl_path), val_lbl_dir / lbl_path.name)

print(f"Done! train: {len(list(train_img_dir.glob('*.*')))} | val: {len(list(val_img_dir.glob('*.*')))}")