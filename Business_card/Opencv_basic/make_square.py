import numpy as np
import cv2
from matplotlib import pyplot as plt

def make_square():
    imagefile = "images/contour2.png"
    img = cv2.imread(imagefile)
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()

    edge = cv2.Canny(grayImg, 100, 200)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]

    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
    epsilon = 0.1 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    cv2.drawContours(img2, [approx], -1, (0, 255, 0), 3)

    cv2.imshow('edge', edge)
    cv2.imshow('img', img)
    cv2.imshow('img2', img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    make_square()