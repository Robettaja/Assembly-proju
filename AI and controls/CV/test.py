import cv2 as cv
import time
import subprocess
import cv2.aruco as aruco
from ultralytics import YOLO
import numpy as np
import sys


rtsp = "rtsp://raspberrypi:8554/cam1"

cmd = [
    "ffmpeg",
    "-rtsp_transport",
    "tcp",
    "-fflags",
    "nobuffer",
    "-flags",
    "low_delay",
    "-probesize",
    "1080",
    "-analyzeduration",
    "0",
    "-flags",
    "low_delay",
    "-i",
    rtsp,
    "-f",
    "rawvideo",
    "-pix_fmt",
    "bgr24",
    "-",
]

width = 640
height = 480
frame_size = width * height * 3

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=frame_size)


params = aruco.DetectorParameters()
tag = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25H9)
detector = aruco.ArucoDetector(tag, params)


while True:
    timer = time.time()
    if process.stdout:
        raw_frame = process.stdout.read(frame_size)
        if len(raw_frame) != frame_size:
            print("Frame incomplete or stream ended")
            break

        # Convert to NumPy array and reshape
        frame = np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))

        # Display the frame
        cv.imshow("FFmpeg RTSP Stream", frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break
