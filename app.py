# app.py
import streamlit as st
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np
import os

# --- CONFIG ---
MODEL_PATH = "runs/detect/train8/weights/best.pt"
CONF_THRESHOLD = 0.25

st.set_page_config(
    page_title="Surface Defect Detector",
    page_icon="magnifying glass",
    layout="centered"
)

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found at {MODEL_PATH}")
        st.stop()
    return YOLO(MODEL_PATH)

model = load_model()

st.title("Surface Defect Detector")
st.write("Upload an image of a metal/plastic part to detect **scratches** and **dents**.")

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "bmp"],
    help="Supported: JPG, PNG, BMP"
)

if uploaded_file is not None:
    # Load image
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Convert to BGR for OpenCV
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_cv = img_array

    # --- INFERENCE ---
    with st.spinner("Detecting defects..."):
        results = model(img_cv, conf=CONF_THRESHOLD, imgsz=640)[0]

    # --- DRAW BOXES ---
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf.item()
        cv2.rectangle(img_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Defect {conf:.2f}"
        cv2.putText(img_cv, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.p