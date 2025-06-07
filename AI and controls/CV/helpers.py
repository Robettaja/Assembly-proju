import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


def preprocessImage(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    image = cv.equalizeHist(image)

    image = cv.GaussianBlur(image, (11, 11), 0)

    ret, image = cv.threshold(image, 40, 255, cv.THRESH_BINARY)

    return image
