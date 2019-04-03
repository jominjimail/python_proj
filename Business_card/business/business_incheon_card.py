import numpy as np
import cv2

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

imgfile = 'images/incheoner.jpeg'
img = cv2.imread(imgfile, cv2.IMREAD_COLOR)
orig = img.copy()

r = 800.0 / img.shape[0]
dim = (int(img.shape[1] * r), 800)
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgray = cv2.GaussianBlur(imgray, (3,3), 0)

edge = cv2.Canny(imgray, 70, 200)
contours, hierarchy = cv2.findContours(edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

#contourArea() and arcLength() is function for closed figure
#when i wrote key=cv2.contourArea(), TypeError: Required argument 'contour' (pos 1) not found call..
i=0
for c in cnts:
    epsilon = 0.02 * cv2.arcLength(c, True)
    #approx is vertex index
    approx = cv2.approxPolyDP(c, epsilon, True)

    cv2.drawContours(img, c, -1, (0, 255, 0), 3)

    #because business card is square
    if len(approx) == 4:
        square = approx
        break


cv2.drawContours(img, [square], -1, (0,255,0), 2)
#cv2.imshow('warp ', img)
rect = order_points(square.reshape(4,2) / r)
(topLeft, topRight, bottomLeft, bottomRight) = rect

w1 = abs(bottomRight[0] - bottomLeft[0])
w2 = abs(topRight[0] - topLeft[0])
h1 = abs(topRight[1] - bottomRight[1])
h2 = abs(topLeft[1] - bottomLeft[1])
maxWidth = max([w1, w2])
maxHeight = max([h1, h2])

dst = np.float32([[0,0], [maxWidth-1, 0], [maxWidth-1, maxHeight-1], [0, maxHeight-1]])

M = cv2.getPerspectiveTransform(rect, dst)
result = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
fin = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

cv2.imshow('original',img)
cv2.imshow('fin', fin)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
