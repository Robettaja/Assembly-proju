# 🏎️ RC Car Racing Tool with BLE + AprilTag 25h9

This project enables real-time racing of RC cars using BLE controllers, AprilTag 25h9 visual tracking, and joystick input. The system tracks lap times, checkpoints, and manages BLE-controlled car movement.

---

## 📸 Marker Generation (Required!)

Generate your **AprilTag 25h9** marker here:  
👉 [https://chev.me/arucogen/](https://chev.me/arucogen/)

- **Tag Family:** `25h9`
- **Size:** `100mm`  
  Print and attach the tag to your RC car.

---

## 🚀 Features

- BLE control of RC cars
- Joystick-based driving
- AprilTag 25h9 tracking
- Lap timing and race progression
- RTSP stream analysis
- Automatic track and checkpoint detection

## Important files

```
```
```
Assembly-proju/
    └── ai_and_controls/
        └── Controls_test/
            ├── 🐍 race_main.py
            ├── 🐍 track_vision.py  
            └── 📁 test_data/
```
---

## 🧰 Requirements

### ✅ Python Version

- Python 3.10 or higher

### 📦 Install Dependencies

Install all required packages via pip:

```bash
pip install bleak pygame opencv-python numpy requests

```

## Setup Instructions

- Attach the AprilTag 25h9 marker to your RC car.
- Setup camera and track without anything on track
- Generate track data running `python track_vision.py `
- Start race using `python race_main.py`
