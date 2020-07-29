# 필요한 패키지를 import함
from __future__ import print_function
import argparse
import cv2
import matplotlib.pylab as plt
#from matplotlib import pyplot as plt

def histogram(img):
	length = len(img.shape)
	hist = []

	# 그레이스케일
	if length==2:
		gray = cv2.calcHist([img], [0], None, [256], [0, 256])
		hist.append(gray)

	# 칼라
	elif length==3:
		for idx in range(3):
			element=cv2.calcHist([img], [idx], None, [256], [0, 256])
			hist.append(element)

	return hist

if __name__ == '__main__' :
	# 명령행 인자 처리
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', '--image', required = True, \
			help = 'Path to the input image')
	ap.add_argument('-t', '--histogram_type', \
			type = int, required = True, \
			help = 'histogram type(1: grayscale, 3: color')
	args = vars(ap.parse_args())

	filename = args['image']
	histogram_type = args['histogram_type']

	# OpenCV를 사용하여 영상 데이터 로딩
	image = cv2.imread(filename)

	if histogram_type == 1:
		# Grayscale 영상으로 변환
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# 히스토그램 계산
	hist = histogram(image)

	# 히스토그램 출력
	if len(hist) == 1: 
		plt.subplot(1, 2, 1), plt.imshow(image, 'gray')
		plt.title('image'), plt.xticks([]), plt.yticks([])
		plt.subplot(1, 2, 2), plt.plot(hist[0])
		plt.title('histogram'), plt.xlim([0,256])
	else:
		color = ('b', 'g', 'r')
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		plt.subplot(1, 2, 1), plt.imshow(image)
		plt.title('image'), plt.xticks([]), plt.yticks([])
		for n, col in enumerate(color):
		    plt.subplot(1, 2, 2)
		    plt.plot(hist[n], color = col)
		plt.title('histogram'), plt.xlim([0,256])
	plt.show()