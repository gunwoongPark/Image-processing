from __future__ import print_function
import cv2
import numpy as np
import argparse

if __name__ == "__main__" :
    # 명령행 인자 처리
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required = True, \
            help = 'Path to the input image')
    args = vars(ap.parse_args())

    filename = args['image']

    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 0, 255)

    (contours, _) = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for idx in range(5):
        cntr = sorted(contours, key=cv2.contourArea, reverse=True)[idx]
        epsilon = 0.01 * cv2.arcLength(cntr, True)
        approx = cv2.approxPolyDP(cntr, epsilon, True)
        if len(approx) == 4:
            break

    pts1 = np.float32([approx[3][0], approx[0][0], approx[2][0], approx[1][0]])
    pts2 = np.float32([[0,0], [480,0], [0,720], [480,720]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(gray, matrix, (480, 720))

    dst = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,21, 5)

    cv2.imshow('dst', dst)
    cv2.waitKey(0)