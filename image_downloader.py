import argparse
import requests
from image_utils.image_processor import Image_Processor


ap = argparse.ArgumentParser(description='Download picture from url and process it.')
ap.add_argument('image_url', help='URL path to the picture.')
ap.add_argument('-g', '--gray', action='store_true', 
                help='change image to gray scale')
ap.add_argument('-b', '--binary', type=int, 
                help='set binary threshold. Integer number 0-255')
ap.add_argument('-rc', '--reverse_colors', action='store_true',
                help='reverse colors')
ap.add_argument('-r', '--rotate', type=int, choices=[90, 180, 270],
                help='rotate clockwise by 90, 180 or 270 degrees')
ap.add_argument('-c', '--cut', nargs='+', type=int,
                help="cut part of picture specified by pixel top left, and bottom right.\
                Usage example '-c 10, 5, 150, 200' this will cut image part\
                from pixel width: 10 and height: 5 to pixel width: 150 heigth: 200,\
                where pixel 0, 0 being top left of the image")

args = ap.parse_args()

# create image processing object, and initialize it with image url
image_processor = Image_Processor()
image_processor.download_image(args.image_url)

# go through all user-selected options and process image accordingly
for argument in vars(args):

    # if the value of argument is not None or False (it was selected by user)
    value = getattr(args, argument)
    if value:
        if argument == 'gray':
            image_processor.to_gray()
            
        elif argument == 'binary':
            image_processor.binary_threshold(value)
            
        elif argument == 'reverse_colors':
            image_processor.reverse_colors()
            
        elif argument == 'rotate':
            image_processor.rotate(value)
            
        elif argument == 'cut':
            image_processor.cut(value)

image_processor.show_images()