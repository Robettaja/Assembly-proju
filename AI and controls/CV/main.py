import cv2 as cv
import cv2.aruco as aruco
import numpy as np
import matplotlib.pyplot as plt
import helpers as help

img = cv.imread("Media/track.jpg")

preprocessed = help.preprocessImage(img)


def get_track(processed_img):
    edges = cv.Canny(processed_img, 20, 200)
    cv.imshow("Edges", edges)

    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_TC89_L1)
    mask = np.zeros(processed_img.shape, dtype=np.uint8)
    sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)

    cv.drawContours(mask, [sorted_contours[0]], -1, (255, 255, 255), cv.FILLED)
    cv.drawContours(mask, [sorted_contours[2]], -1, (0, 0, 0), cv.FILLED)
    return mask


def get_car(processed_img):
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
    parameters = cv.aruco.DetectorParameters()
    detector = cv.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(processed_img)
    mask = np.zeros(processed_img.shape, dtype=np.uint8)
    if ids is not None:
        for marker_corners in corners:
            pts = marker_corners[0].astype(np.int32)
            return cv.fillConvexPoly(mask, pts, 255)


def is_car_in_track(track_mask, car_mask):
    return cv.countNonZero(cv.bitwise_and(track_mask, car_mask)) > 0


track_mask = get_track(preprocessed)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Track Mask", img)

car_mask = get_car(gray)
print("Is car in track:", is_car_in_track(track_mask, car_mask))

cv.waitKey(0)
