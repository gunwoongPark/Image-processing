# 필요한 패키지를 import함
from __future__ import print_function
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt

def findContours(bin):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

    img = cv2.morphologyEx(bin, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    (contours, hierarchy) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return img, contours

if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, \
                    help = 'Path to the input image')
    args = vars(ap.parse_args())

    filename = args['image']

    image = cv2.imread(filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    bin = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 2)

    contour_img, contours = findContours(bin)

    new_img = np.zeros_like(contour_img, dtype="uint8")
    for idx in range (len(contours)):
        cntr = sorted(contours, key=cv2.contourArea, reverse=True)[idx]
        cv2.drawContours(new_img, [cntr], 0, (255,255,255), -1)

    plt.subplot(1,3,1), plt.imshow(gray, cmap='gray')
    plt.title('grayscale and blur'), plt.xticks([]), plt.yticks([])

    plt.subplot(1,3,2), plt.imshow(bin, cmap='gray')
    plt.title('threshold'), plt.xticks([]), plt.yticks([])

    plt.subplot(1,3,3), plt.imshow(new_img, cmap='gray')
    plt.title('contour'), plt.xticks([]), plt.yticks([])

    plt.show()