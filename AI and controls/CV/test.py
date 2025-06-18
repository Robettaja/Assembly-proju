import cv2 as cv
import time
from cv2 import aruco
from ultralytics import YOLO
import numpy as np
import sys


cap = cv.VideoCapture("rtsp://raspberrypi:8554/cam1")
model = YOLO("best.pt")

params = aruco.DetectorParameters()
tag = aruco.getPredefinedDictionary(aruco.DICT_APRILTAG_25H9)
detector = aruco.ArucoDetector(tag, params)

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print(f"Width: {width}, Height: {height}")


while True:
    timer = time.time()
    ret, frame = cap.read()
    results = list(model(frame, stream=True))
    annotated_frame = results[0].plot()
    fps = 1 / (time.time() - timer)

    cv.putText(
        annotated_frame,
        f"FPS: {fps:.2f}",
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv.imshow("Frame", annotated_frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
