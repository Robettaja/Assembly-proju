import cv2 as cv
import numpy as np
import sys

cap = cv.VideoCapture("rtsp://raspberrypi:8554/cam1")
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

print(f"Width: {width}, Height: {height}")

while True:
    ret, frame = cap.read()
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("Frame", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
