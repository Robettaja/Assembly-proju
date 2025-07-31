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

##   Setup Instructions

1. Attach the AprilTag 25h9 marker
Securely place the AprilTag 25h9 marker on your RC car to enable accurate tracking.

2. Set up the camera and track
Position your camera to cover the entire track area. Make sure the track is clear — no obstacles or objects on it.

3. Generate track data
Run the following command to capture and process the track layout:
```bash
python track_vision.py
```
4. Start the race
Once the track data is generated, launch the race with:
```bash
python race_main.py
