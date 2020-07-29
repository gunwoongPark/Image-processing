from __future__ import print_function
import argparse
import numpy as np
import cv2
import os
import glob
import time

def detectBarcode(image):
    sobelx = cv2.Sobel(image, cv2.CV_8U, 1, 0, ksize=-1)
    sobely = cv2.Sobel(image, cv2.CV_8U, 0, 1, ksize=-1)

    hori_dst = cv2.subtract(sobelx, sobely)
    vert_dst = cv2.subtract(sobely, sobelx)

    hori_dst = cv2.GaussianBlur(hori_dst, (5, 5), 0)
    vert_dst = cv2.GaussianBlur(vert_dst, (5, 5), 0)

    hori_th, hori_dst = cv2.threshold(hori_dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    vert_th, vert_dst = cv2.threshold(vert_dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 직사각형 모양으로 닫힘
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (93, 1))
    vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 93))

    hori_dst = cv2.morphologyEx(hori_dst, cv2.MORPH_CLOSE, hori_kernel)
    vert_dst = cv2.morphologyEx(vert_dst, cv2.MORPH_CLOSE, vert_kernel)

    # 작은 사각형 모양으로 침식->팽창 노가다
    small_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))

    hori_dst = cv2.erode(hori_dst, small_rect, iterations=12)
    hori_dst = cv2.dilate(hori_dst, small_rect, iterations=12)

    vert_dst = cv2.erode(vert_dst, small_rect, iterations=12)
    vert_dst = cv2.dilate(vert_dst, small_rect, iterations=12)

    (contours, hierarchy) = cv2.findContours(hori_dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cntr = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        hori_points = cv2.boundingRect(cntr)
    else:
        hori_points = [0, 0, 0, 0]

    (contours, hierarchy) = cv2.findContours(vert_dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cntr = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        vert_points = cv2.boundingRect(cntr)
    else:
        vert_points = [0, 0, 0, 0]

    hori_size = hori_points[2] * hori_points[3]
    vert_size = vert_points[2] * vert_points[3]

    if hori_size > vert_size:
        points = hori_points
    else:
        points = vert_points

    return (points[0], points[1], points[0] + points[2], points[1] + points[3])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required = True, help = "path to the dataset folder")
    ap.add_argument("-r", "--detectset", required = True, help = "path to the detectset folder")
    ap.add_argument("-f", "--detect", required = True, help = "path to the detect file")
    args = vars(ap.parse_args())
    
    dataset = args["dataset"]
    detectset = args["detectset"]
    detectfile = args["detect"]

    # 결과 영상 저장 폴더 존재 여부 확인
    if(not os.path.isdir(detectset)):
        os.mkdir(detectset)

    # 결과 영상 표시 여부
    verbose = False

    # 검출 결과 위치 저장을 위한 파일 생성
    f = open(detectfile, "wt", encoding="UTF-8")  # UT-8로 인코딩

    start = time.time()

    # 바코드 영상에 대한 바코드 영역 검출
    for imagePath in glob.glob(dataset + "/*.jpg"):
        print(imagePath, '처리중...')

        # 영상을 불러오고 그레이 스케일 영상으로 변환
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 바코드 검출

        points = detectBarcode(gray)

        # 바코드 영역 표시
        detectimg = cv2.rectangle(image, (points[0], points[1]), (points[2], points[3]), (0, 255, 0), 2)  # 이미지에 사각형 그리기

        # 결과 영상 저장
        loc1 = imagePath.rfind("\\")
        loc2 = imagePath.rfind(".")
        fname = 'result/' + imagePath[loc1 + 1: loc2] + '_res.jpg'
        cv2.imwrite(fname, detectimg)

        # 검출한 결과 위치 저장
        #print(imagePath[loc1 + 1: loc2], len(imagePath[loc1 + 1: loc2]))
        f.write(imagePath[loc1 + 1: loc2])
        f.write("\t")
        f.write(str(points[0]))
        f.write("\t")
        f.write(str(points[1]))
        f.write("\t")
        f.write(str(points[2]))
        f.write("\t")
        f.write(str(points[3]))
        f.write("\n")

        if verbose:
            cv2.imshow("image", image)
            cv2.waitKey(0)
    end = time.time()
    print('소요 시간 : {}'.format(end-start))