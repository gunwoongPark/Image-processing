from __future__ import print_function
import numpy as np
import argparse
import array
import PPM.PPM_P6 as ppm

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required = True, \
                help = 'Path to the input image')
ap.add_argument('-o', '--output', required = True, \
                help = 'Path to the output image')
ap.add_argument('-l', '--location', type = int, \
                nargs='+', default = [0,0], \
                help = 'Location of the rectangle image')
ap.add_argument('-s', '--size', type = int, \
                nargs='+', default = [50,50], \
                help = 'Size of the rectangle image')
ap.add_argument('-c', '--color', type = int, \
                nargs='+', default = [255,0,0], \
                help = 'Color of the rectangle image')

ppm_p6 = ppm.PPM_P6()

args = vars(ap.parse_args())

infile = args['input']

(width, height, maxval, bitmap) = ppm_p6.read(infile)

outfile = args['output']
rect_location = args['location']
rect_color = args['color']
rect_size = args['size']

ori_image = array.array('B',bitmap)
ori_image = np.array(ori_image)

ori_image = ori_image.reshape((height,width,3))

ori_image[rect_location[0]:rect_location[0]+rect_size[1], rect_location[1]:rect_location[1]+rect_size[0]] = [rect_color[0], rect_color[1],rect_color[2]]

ori_image = ori_image.reshape(height*width*3)
ori_image = bytes(ori_image)

ppm_p6.write(width, height, maxval, ori_image, outfile)

