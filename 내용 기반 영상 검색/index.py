from __future__ import print_function
import argparse
import cv2
import pickle
import glob

def histogram1D(img):
	hist = cv2.calcHist([img], [0], None, [256], [0, 256])
	hist = cv2.normalize(hist, hist)
	return hist

def histogram2D(img):
	hist = cv2.calcHist( [img], [0, 1], None, [180, 256], [0, 180, 0, 256] )
	hist = cv2.normalize(hist, hist)
	return hist

def histogram3D(img):
    hist = cv2.calcHist([img], [0, 1, 2], None, [32, 32, 32], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist)
    return hist

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Folder containing images to be indexed.')
    ap.add_argument('-i', '--index', required=True, help='A file that stores the index you created.')
    ap.add_argument('-t', '--type', required=True, help='histogram method.', type=int)
    args = vars(ap.parse_args())

    dataset = args['dataset']
    index = args['index']
    type = args['type']

    file = open(index, 'wb')

    result = {}

    print('인덱스 파일 생성중..')

    for imagePath in glob.glob(dataset + "/*.jpg"):

        image = cv2.imread(imagePath)

        if type == 1:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv_image)
            histogram = histogram1D(h)
        elif type == 2:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            histogram = histogram2D(hsv_image)
        else :
            histogram = histogram3D(image)


        loc1 = imagePath.rfind('\\')
        loc2 = imagePath.rfind('.')

        result[imagePath[loc1 + 1: loc2]] = histogram

    pickle.dump(result, file)

    print('생성 완료!')