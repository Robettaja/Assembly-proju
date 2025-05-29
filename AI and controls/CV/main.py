import cv2 as cv
import numpy as np

img = cv.imread("Media/neuronmonke.jpg")

cany = cv.Canny(img, 125, 175)


cv.imshow("monke", cany)
cv.waitKey(0)

