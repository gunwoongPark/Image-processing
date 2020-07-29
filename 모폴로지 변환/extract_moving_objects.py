from __future__ import print_function
import argparse
import numpy as np
import cv2

def movingObjectsDetect(fgmask):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

    img = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    (contours, hierarchy) = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return img, contours

if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--video', required=False,\
                    help ='Path to the video file')
    args = vars(ap.parse_args())

    fvideo = args.get("video")

    if fvideo is None:
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(args['video'])

    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        (retval, frame) = camera.read()

        if fvideo is not None and not retval:
            break

        fgmask = fgbg.apply(frame)

        contour_img, contours = movingObjectsDetect(fgmask)

        new_img = np.zeros_like(contour_img, dtype="uint8")
        for idx in range(len(contours)):
            cntr = sorted(contours, key=cv2.contourArea, reverse=True)[idx]
            cv2.drawContours(new_img, [cntr], 0, (255,255,255), -1)

        new_img = cv2.cvtColor(new_img, cv2.COLOR_GRAY2RGB)

        result = np.hstack((frame,new_img))

        cv2.imshow('frame', result)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()