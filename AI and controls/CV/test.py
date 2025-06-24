import cv2 as cv
import time
import cv2.aruco as aruco
from ultralytics import YOLO
import numpy as np
import sys


cap = cv.VideoCapture("rtsp://raspberrypi:8554/cam1")
model = YOLO("best.pt")

params = aruco.DetectorParameters()
tag = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
detector = aruco.ArucoDetector(tag, params)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print(f"Width: {width}, Height: {height}")


while True:
    timer = time.time()
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
    fps = 1 / (time.time() - timer)

    cv.putText(
        frame,
        f"FPS: {fps:.2f}",
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv.imshow("Frame", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
