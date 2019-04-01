import numpy as np
import cv2

def warpPerspective():
    img = cv2.imread("images/transform.jpg")

    topLeft = [127, 157]
    topRight = [448, 152]
    bottomLeft = [579, 526]
    bottomRight = [54, 549]

    pts1 = np.float32([topLeft, topRight, bottomLeft, bottomRight])

    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])
    minWidth = min(w1, w2)
    minHeight = min(h1, h2)

    # the standard is min not Max reduce the size is more easy?
    pts2 = np.float32([[0, 0], [minWidth-1, 0], [minWidth-1, minHeight - 1], [0, minHeight-1]])

    # getPerspectiveTransform  vs. getAffineTransform (only move pixel but pers~ consider perspective)
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, M, (int(minWidth), int(minHeight)))

    cv2.imshow('original', img)
    cv2.imshow('warp Transform', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == "__main__":
    warpPerspective()