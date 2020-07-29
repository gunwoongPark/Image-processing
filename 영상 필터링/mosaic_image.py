from __future__ import print_function
import argparse
import cv2
import numpy as np
import random
from handle_channel_roi import display_image

def mosaic_image(img, rect, size, mtype):
    new_result = img.copy()
    for height in range (rect[0], rect[2], size[0]):
        for width in range (rect[1], rect[3], size[1]):

            # 모자이크 크기만큼 슬라이싱
            dst = img[height:height+size[0], width:width+size[1]]

            # 평균
            if mtype == 1:
                dst = np.mean(dst, 1)
                dst = np.mean(dst, 0)
                new_result[height:height+size[0],width:width+size[1]] =\
                    [dst[0], dst[1], dst[2]]

            # 최대값
            elif mtype == 2:
                dst = np.max(dst, 1)
                dst = np.max(dst, 0)
                new_result[height:height + size[0], width:width + size[1]] = \
                    [dst[0], dst[1], dst[2]]

            # 최소값
            elif mtype == 3:
                dst = np.min(dst,1)
                dst = np.min(dst,0)
                new_result[height:height + size[0], width:width + size[1]] = \
                    [dst[0], dst[1], dst[2]]

            # 랜덤
            elif mtype ==4:
                # 수평 방향 넘칠 경우
                if height + size[0] > rect[2]:
                    new_height = random.randrange(height, rect[2])
                # 딱 떨어질 경우
                else :
                    new_height = random.randrange(height, height+size[0])
                # 수직 방향 넘칠 경우
                if width+size[1] > rect[3]:
                    new_width = random.randrange(width, rect[3])
                # 딱 떨어질 경우
                else:
                    new_width = random.randrange(width, width+size[1])
                # 처
                new_result[height:height+size[0], width:width+size[1]] = \
                    img[new_height][new_width]

    return new_result
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, \
                    help = "Path to the input image")
    ap.add_argument("-s", "--start_point", type = int, \
                    nargs='+', default = [0,0], \
                    help = "Start point of the rectangle")
    ap.add_argument("-e", "--end_point", type = int, \
                    nargs='+', default=[150,100], \
                    help = "End point of the rectangle")
    ap.add_argument("-z", "--size", type = int, \
                    nargs='+', default=[15,15], \
                    help = "Mosaic Size")
    ap.add_argument("-t", "--type", type= int, \
                    default=1, \
                    help = "Mosaic Size")
    args = vars(ap.parse_args())

    filename = args['image']
    sp = args['start_point']
    ep = args['end_point']
    size = args['size']
    mtype = args['type']

    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    if(image is None):
        raise IOError("Cannot open the image")

    # 유효한 이미지 여부 확인
    (rows, cols, _)= image.shape
    if(sp[0]<0 or sp[1]<0 or ep[0] > rows or ep[1]>cols):
        raise ValueError('Invalid Size')

    rect = sp + ep

    result = mosaic_image(image, rect, size, mtype)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()