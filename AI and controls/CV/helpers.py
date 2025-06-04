import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


def preprocessImage(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    image = cv.GaussianBlur(image, (5, 5), 0)

    ret, image = cv.threshold(image, 125, 255, cv.THRESH_BINARY)

    return image


def histogramEqualization(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    hist = cv.calcHist([gray], [0], None, [256], [0, 256])
    cdf = hist.cumsum()

    plt.plot(cdf, color="b")
    plt.xlim([0, 256])
    plt.show()

    return gray
