# Surface Defect Detector

![YOLOv8 Badge](https://img.shields.io/badge/YOLOv8-Defect%20Detection-brightgreen)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-black?logo=streamlit)](https://yourusername-defect-detector-app.streamlit.app)

A **YOLOv8-powered web application** for detecting **scratches and dents** on metal/plastic parts. Trained on NEU Surface Defect + DAGM 2007 datasets, achieving **96.0% mAP@0.5 accuracy**. Upload an image → Get instant bounding boxes with confidence scores.

## 🎯 Features
- **Real-time Detection**: Upload JPG/PNG/BMP images for YOLOv8 inference.
- **Visual Output**: Green bounding boxes + confidence labels on defects.
- **Binary Classification**: Treats all defects (crazing, pitted, scratches) as one class.
- **Deployed & Free**: Live demo on Streamlit Cloud—no install needed.
- **Edge-Ready**: Lightweight model (6MB) for production/edge devices.

## 📊 Performance
- **Dataset**: ~1,439 labeled images (NEU + DAGM Class 1).
- **Metrics** (Validation Set):
  | Metric       | Value  |
  |--------------|--------|
  | mAP@0.5     | 96.0% |
  | mAP@0.5:0.95| 62.0% |
  | Precision   | 95.1% |
  | Recall      | 92.3% |
  | FPS (CPU)   | ~15   |

- **Training**: 50 epochs on Intel i7 CPU, batch=8, lr=0.001.

## 🚀 Live Demo
[![Deployed on Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.png)](https://yourusername-defect-detector-app.streamlit.app)

**Test it now**: Upload a sample metal surface image → See detections in seconds!

## 🛠️ Local Setup
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/yourusername/defect-detector-app.git
   cd defect-detector-app