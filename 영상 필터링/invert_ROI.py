# 필요한 패키지를 import함
from __future__ import print_function
import argparse
import cv2
import numpy as np
from handle_channel_roi import display_image

# 픽셀 접근
def invert_image_m1(img, rect):
	dst = img.copy()
	length = len(img.shape)

	#그레이스케일
	if length == 2:
		idx = rect[0]
		jdx = rect[1]
		for i in range(idx, rect[2]):
			for j in range(jdx, rect[3]):
				dst[j,i] = 255-dst[j,i]
		print('rect[0]: {}, rect[1]: {}'.format(rect[0], rect[1]))
		return dst

	#칼라영상
	elif length == 3:
		idx = rect[0]
		jdx = rect[1]
		for i in range(idx, rect[2]):
			for j in range(jdx, rect[3]):
				dst[j, i, 0] = 255 - dst[j, i, 0]
				dst[j, i, 1] = 255 - dst[j, i, 1]
				dst[j, i, 2] = 255 - dst[j, i, 2]
		print('rect[0]: {}, rect[1]: {}'.format(rect[0], rect[1]))
		return dst

# 슬라이싱
def invert_image_m2(img, rect):
	dst = img.copy()
	dst[rect[1]:rect[3], rect[0]:rect[2]] = 255 - dst[rect[1]:rect[3], rect[0]:rect[2]]
	return dst

if __name__ == '__main__' :
	# 명령행 인자 처리
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required = True, \
			help = "Path to the input image")
	ap.add_argument("-s", "--start_point", type = int, \
 			nargs='+', default=[0, 0], \
			help = "Start point of the rectangle")
	ap.add_argument("-e", "--end_point", type = int, \
	 		nargs='+', default=[150, 100], \
			help = "End point of the rectangle")
	args = vars(ap.parse_args())

	filename = args["image"]
	sp = args["start_point"]
	ep = args["end_point"]

	# OpenCV를 사용하여 영상 데이터 로딩
	image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
	# (rows, cols, _) = image.shape
	# if(sp[0] < 0 or sp[1] < 0 or ep[0] > rows or ep[1] > cols):
	# 	raise ValueError('Invalid Size')

	# list 연결
	rect = sp + ep

	e1 = cv2.getTickCount()
	inverted = invert_image_m1(image, rect)
	e2 = cv2.getTickCount()
	time = (e2 - e1)/ cv2.getTickFrequency()
	print('[정보]방법 1 소요시간: {}'.format(time))

	display_image(inverted, 'inverted')

	e1 = cv2.getTickCount()
	inverted = invert_image_m2(image, rect)
	e2 = cv2.getTickCount()
	time = (e2 - e1)/ cv2.getTickFrequency()
	print('[정보]방법 2 소요시간: {}'.format(time))


	display_image(inverted, 'inverted')