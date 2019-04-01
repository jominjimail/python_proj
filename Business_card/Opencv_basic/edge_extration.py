import numpy as np
import cv2
from matplotlib import pyplot as plt

#Find & Draw Contours

def contour():
    imgfile = "images/document2.jpg"
    img = cv2.imread(imgfile)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #canny detection algorighm
    edge = cv2.Canny(imgray, 100, 200)
    #In OpenCV 2, findContours returns just two values, contours and hierarchy
    #image , contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('edge', edge)

    #draw contour
    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    cv2.imshow('image', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    contour()
