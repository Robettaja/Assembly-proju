import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import helpers as help

img = cv.imread("Media/shapefloor.jpg")
img = cv.resize(img, (640, 480))

preprocessed = help.preprocessImage(img)

edges = cv.Canny(preprocessed, 100, 200)

contours, hierarchy = cv.findContours(
    preprocessed, cv.RETR_CCOMP, cv.CHAIN_APPROX_TC89_L1
)
print(f"Number of contours found: {len(contours)}")
mask = np.zeros(preprocessed.shape, dtype=np.uint8)
sorted_contours = sorted(contours, key=cv.contourArea, reverse=True)

cv.drawContours(mask, [sorted_contours[1]], -1, (255, 255, 255), cv.FILLED)
cv.imshow("", mask)


cv.waitKey(0)
