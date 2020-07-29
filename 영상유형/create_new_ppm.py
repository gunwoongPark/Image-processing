from __future__ import print_function
import argparse
import PPM.PPM_P6 as ppm

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required = True, \
                help = 'Path to the output image')
ap.add_argument('-s', '--size', type = int, \
                nargs='+', default = [50,30], \
                help = 'Size of the output image')
ap.add_argument('-c', '--color', type = int, \
                nargs='+', default = [255,255,255], \
                help = 'Color of the output image')

args = vars(ap.parse_args())

outfile = args['output']
color = args['color']
size = args['size']

width = size[0]
height = size[1]
maxval = 255
colors = color*width*height*3

ppm_p6 = ppm.PPM_P6()

ppm_p6.write(width, height, maxval, colors, outfile)

