# fix_dataset.py (FINAL – CASE INSENSITIVE)
import os, shutil, cv2, glob, xml.etree.ElementTree as ET
from pathlib import Path

print("DEBUG + CASE-INSENSITIVE CONVERSION...\n")

for split in ['train', 'val']:
    os.makedirs(f'data/yolo/{split}/images', exist_ok=True)
    os.makedirs(f'data/yolo/{split}/labels', exist_ok=True)

# === 1. NEU: ACCEPT ANY CLASS + CASE-INSENSITIVE .jpg ===
neu_converted = 0
for split in ['train', 'val']:
    img_dir = f'data/NEU-DET/{split}/images'
    ann_dir = f'data/NEU-DET/{split}/annotations'
    if not os.path.exists(img_dir): continue
    print(f"\nConverting NEU {split}...")

    for img_path in glob.glob(f'{img_dir}/*.[jJ][pP][gG]'):  # ← FIXED
        xml_path = img_path.replace('/images/', '/annotations/')
        # Try .xml, .XML, .Xml
        base = Path(img_path).stem
        xml_candidates = [f'{ann_dir}/{base}.xml', f'{ann_dir}/{base}.XML']
        xml_path = next((p for p in xml_candidates if os.path.exists(p)), None)
        if not xml_path: continue

        img = cv2.imread(img_path)
        if img is None: continue
        h, w = img.shape[:2]
        tree = ET.parse(xml_path); root = tree.getroot()
        boxes = []
        for obj in root.iter('object'):
            name = obj.find('name').text
            # ACCEPT ANY CLASS
            b = obj.find('bndbox')
            x1 = int(b.find('xmin').text)
            y1 = int(b.find('ymin').text)
            x2 = int(b.find('xmax').text)
            y2 = int(b.find('ymax').text)
            cx = (x1 + x2) / (2 * w)
            cy = (y1 + y2) / (2 * h)
            bw = (x2 - x1) / w
            bh = (y2 - y1) / h
            boxes.append(f"0 {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

        if boxes:
            base = Path(img_path).stem
            ext = Path(img_path).suffix
            shutil.copy(img_path, f'data/yolo/{split}/images/{base}{ext}')
            with open(f'data/yolo/{split}/labels/{base}.txt', 'w') as f:
                f.write('\n'.join(boxes))
            neu_converted += 1
            if neu_converted <= 3:
                print(f"   Saved: {base}{ext} ({len(boxes)} boxes)")

print(f"\nNEU: {neu_converted} images with defects")

# === 2. DAGM: CASE-INSENSITIVE .PNG + NON-BLACK MASK ===
dagm_converted = 0
for typ in ['Train', 'Test']:
    split = 'train' if typ == 'Train' else 'val'
    img_dir = f'data/CompetitionData/Class1/{typ}/Good'
    lbl_dir = f'data/CompetitionData/Class1/{typ}/Label'

    if not os.path.exists(img_dir) or not os.path.exists(lbl_dir): continue
    print(f"\nConverting DAGM {typ}...")

    for img_path in glob.glob(f'{img_dir}/*.[pP][nN][gG]'):  # ← FIXED
        lbl_path = os.path.join(lbl_dir, Path(img_path).name)
        if not os.path.exists(lbl_path): continue

        img = cv2.imread(img_path)
        mask = cv2.imread(lbl_path, 0)
        if img is None or mask is None: continue
        if mask.max() == 0: continue

        h, w = img.shape[:2]
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            if bw < 3 or bh < 3: continue
            cx = (x + bw/2) / w
            cy = (y + bh/2) / h
            boxes.append(f"0 {cx:.6f} {cy:.6f} {bw/w:.6f} {bh/h:.6f}")

        if boxes:
            base = Path(img_path).stem
            ext = Path(img_path).suffix
            shutil.copy(img_path, f'data/yolo/{split}/images/{base}{ext}')
            with open(f'data/yolo/{split}/labels/{base}.txt', 'w') as f:
                f.write('\n'.join(boxes))
            dagm_converted += 1
            if dagm_converted <= 3:
                print(f"   Saved: {base}{ext} ({len(boxes)} boxes)")

print(f"\nDAGM: {dagm_converted} images with defects")

# === FINAL ===
train_imgs = len(os.listdir('data/yolo/train/images')) if os.path.exists('data/yolo/train/images') else 0
val_imgs   = len(os.listdir('data/yolo/val/images'))   if os.path.exists('data/yolo/val/images')   else 0
print(f"\nSUCCESS! Dataset ready:")
print(f"   train/images : {train_imgs}")
print(f"   val/images   : {val_imgs}")
print(f"   Total defects: {train_imgs + val_imgs}")