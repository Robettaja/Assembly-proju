import cv2 as cv
import cv2.aruco as aruco
import time
from cv2.gapi import threshold
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt


img = cv.imread("Media/track.jpg")


def aruco_detect(img, aruco_mark_type):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img, (5, 5), 0)
    aruco_dict = aruco.getPredefinedDictionary(aruco_mark_type)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(img)
    mask = np.zeros(img.shape, dtype=np.uint8)
    if ids is not None:
        for marker_corners in corners:
            pts = marker_corners[0].astype(np.int32)
            cv.fillConvexPoly(mask, pts, 255)
    return mask


def is_intersecting(mask1, mask2):
    return cv.countNonZero(cv.bitwise_and(mask1, mask2)) > 0


def get_track_mask(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.GaussianBlur(image, (7, 7), 0)
    edges = cv.Canny(image, 50, 150, apertureSize=3)
    mask = cv.adaptiveThreshold(
        edges, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2
    )
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    parent_contour = sorted_contours[0]
    mask = np.zeros(image.shape, dtype=np.uint8)

    cv.drawContours(mask, [parent_contour], -1, (255, 255, 255), thickness=cv.FILLED)
    cv.drawContours(mask, [sorted_contours[2]], -1, (0, 0, 0), thickness=cv.FILLED)
    cv.imwrite("Track data/track_mask.jpg", mask)


def get_finishline(img):
    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img = cv.GaussianBlur(img, (5, 5), 0)

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv.inRange(img, lower_red1, upper_red1)
    mask2 = cv.inRange(img, lower_red2, upper_red2)
    red_mask = cv.bitwise_or(mask1, mask2)
    red_mask = cv.Canny(red_mask, 50, 150, apertureSize=3)

    contours, _ = cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)
    mask = np.zeros(img2.shape, dtype=np.uint8)
    cv.drawContours(
        mask, [sorted_contours[0]], -1, (255, 255, 255), thickness=cv.FILLED
    )
    cv.imwrite("Track data/finishline_mask.jpg", mask)


def race_loop():
    model = YOLO("yolov8x.pt")
    video = cv.VideoCapture("https://192.168.129.151:8080/video")
    race_mask = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
    finnish_line_mask = cv.imread("Track data/finishline_mask.jpg", cv.IMREAD_GRAYSCALE)
    while True:
        timer = time.time()
        ret, frame = video.read()

        if not ret:
            print("Error: Can't receive frame. Exiting...")
            break

        # Run YOLOv8 detection
        results = model(frame)

        # Draw results on frame
        annotated_frame = results[0].plot()

        # Show the frame
        cv.imshow("YOLOv8 Live Detection", annotated_frame)

        # Break the loop on 'q' key press
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


checkpoints = []

track = cv.imread("Track data/track_mask.jpg", cv.IMREAD_GRAYSCALE)
finish_line = cv.imread("Track data/finishline_mask.jpg", cv.IMREAD_GRAYSCALE)
race_loop()
