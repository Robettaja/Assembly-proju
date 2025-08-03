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
            └── 📁 track_data/
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

## 📃 Setup Instructions

1. Attach the AprilTag 25h9 marker
   Securely place the AprilTag 25h9 marker on your RC car to enable accurate tracking.

2. Set up the camera and track
   Position your camera to cover the entire track area. Make sure the track is clear — no obstacles or objects on it.

3. Generate track data
   Run the following command to capture and process the track layout:

### PLEASE REMOVE EVERYFILE FROM track_data folder before running this command

```bash
python track_vision.py
```

4. Start the race
   Once the track data is generated, launch the race with:

```bash
python race_main.py
```

## ⚠️ Possible Errors and How to Fix Them

### 1. **No BLE Device Found**

- **Cause:** The RC car is not powered on.
- **Fix:**
  - Ensure that RC car is on or correct car is powered. more orange car is not operational.

### 2. **Unable to Connect to BLE Device**

- **Cause:** BLE connection timeout or interference.
- **Fix:**
  - Move closer to the RC car to improve signal strength.
  - Restart the BLE device and your computer/host.
  - Ensure no other device is connected to the RC car’s BLE simultaneously.

### 3. **No Camera Feed / RTSP Stream Not Found**

- **Cause:** Raspberry Pi camera stream is not running.
- **Fix:**
  - Check network connectivity between host and Raspberry Pi.

### 4. **AprilTag Not Detected**

- **Cause:** Tag not visible, or wrong tag family.
- **Fix:**
  - Ensure the AprilTag is firmly attached and fully visible to the camera.
  - Confirm the tag is from the `25h9` family as specified.

### 5. **Joystick Not Detected**

- **Cause:** Joystick is unplugged.
- **Fix:**
  - Plug in the joystick before starting the program.
  - Check your OS recognizes the joystick device.
