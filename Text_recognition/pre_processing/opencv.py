import numpy as np
import cv2

imgfile = '../images/6.jpg'
img = cv2.imread(imgfile, cv2.IMREAD_COLOR)
orig = img.copy()

img = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_AREA)

imgray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#imgray = cv2.GaussianBlur(imgray, (3,3), 0)

kernel_close = np.ones((9, 5), np.uint8)
kernel_gradient = np.ones((2, 2), np.uint8)

mor_result = cv2.morphologyEx(imgray, cv2.MORPH_GRADIENT, kernel_gradient)
adapt_result= cv2.adaptiveThreshold(mor_result, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 10);
mor2_result = cv2.morphologyEx(adapt_result, cv2.MORPH_CLOSE, kernel_close)

contours, hierarchy = cv2.findContours(mor2_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

i=0
for c in contours:
    rect = cv2.boundingRect(c);
    print rect
    x, y, w, h = rect

    if h > 10 and w > 40 and not(w >= 512 - 5 and h >= 512 - 5):
        cv2.rectangle(img, (x,y),(x-w,y-h), (0, 255, 0), 2)


    i = i+1

cv2.imshow('fin..? ', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#
# cv2.imshow('fin', imgray)
# cv2.imshow('after', adapt)
# cv2.waitKey(0)
# cv2.destroyAllWindows()