from __future__ import print_function
import argparse
import cv2
import pickle
from collections import OrderedDict
from matplotlib import pyplot as plt

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

if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dataset', required=True, help='Folder containing images to be indexed.')
    ap.add_argument('-i', '--index', required=True, help='A file that stores the index you created.')
    ap.add_argument('-q', '--query', required=True, help='Input images to be used for queries.')
    ap.add_argument('-t', '--type', required=True, help='Type of dimension', type=int)
    ap.add_argument('-c', '--compare', required=True, help='Type of compare function.', type=int)

    args = vars(ap.parse_args())

    dataset = args['dataset']
    index = args['index']
    query = args['query']
    dim_type = args['type']
    comp_type = args['compare']

    result = {}

    image = cv2.imread(query)

    if dim_type == 1:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        query_hist = histogram1D(h)
    elif dim_type ==2:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        query_hist = histogram2D(hsv_image)
    else:
        query_hist = histogram3D(image)


    with open(index, 'rb') as f:
        hist_result = pickle.load(f)

    for key, values in hist_result.items():
        if comp_type == 1:
            result[key] = cv2.compareHist(hist_result[key], query_hist, cv2.HISTCMP_CORREL)
        elif comp_type==2:
            result[key] = cv2.compareHist(hist_result[key], query_hist, cv2.HISTCMP_CHISQR)
        elif comp_type == 3:
            result[key] = cv2.compareHist(hist_result[key], query_hist, cv2.HISTCMP_INTERSECT)
        else :
            result[key] = cv2.compareHist(hist_result[key], query_hist, cv2.HISTCMP_BHATTACHARYYA)

    if comp_type == 1 or comp_type == 3 :
        sorted_result = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse= True))
    else :
        sorted_result = OrderedDict(sorted(result.items(), key=lambda x: x[1], reverse= False))

    # 상위 6개 이미지 출력 결과
    rate = {0:'first',
            1:'second',
            2:'third',
            3:'fourth',
            4:'fifth',
            5:'sixth'}
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    plt.subplot(2, 6, 1), plt.imshow(image)
    plt.title('query image'), plt.xticks([]), plt.yticks([])

    count = 0
    for key,values in sorted_result.items():
        sub_image = dataset+'\\' + key + '.jpg'
        sub_image = cv2.imread(sub_image)

        sub_image = cv2.cvtColor(sub_image, cv2.COLOR_RGB2BGR)

        plt.subplot(2,6,7+count), plt.imshow(sub_image)
        plt.title(rate[count]), plt.xticks([]), plt.yticks([])

        count +=1
        if count == 6:
            break

    plt.show()

    # 1개씩 늘려가는 결과
    loc1 = query.rfind('\\')
    loc2 = query.rfind('_')

    ori_title = query[loc1 + 1: loc2]

    count = 0

    for top_count in range(1, 11):
        print('top count : {}'.format(top_count))
        stack = 0
        count = 0
        for key, values in sorted_result.items():
            k_loc = key.rfind('_')
            temp = key[:k_loc]
            if temp == ori_title:
                count +=1
            print('key : {}, values : {}'.format(key, values))
            stack += 1
            if stack == top_count:
                break

        precision = float(count / top_count)
        recall = float(count / 9)
        print('precision : {}'.format(precision))
        print('recall : {}'.format(recall))
        print('---------------------------------------------')