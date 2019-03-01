import argparse
from image_utils.image_processor import ImageProcessor

ap = argparse.ArgumentParser(description='Download picture from url and process it.')

# first positional argument will store string image url
ap.add_argument('image_url', help='URL path to the picture.')

# if user will use -g -> 'gray' parameter will be saved as True
ap.add_argument('-g', '--gray', action='store_true',
                help='change image to gray scale')

# user needs to use e.g. -b 120 to specify binary threshold
# this value is clipped to [0, 255] during processing
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
image_processor = ImageProcessor()
image_processor.download_image(args.image_url)

# go through all available options and process image accordingly
# to the way user has chosen. If user didn't choose anything
# this will loop 6 times, but image will not be processed
for argument in vars(args):

    # get parameter of the argument
    value = getattr(args, argument)
    # if the parameter is not None or False -> it was selected by user
    if value not in [None, False]:
        if argument == 'gray':
            image_processor.to_gray()

        elif argument == 'binary':
            # check if binary threshold is in range 0-255
            if not 0 <= value <= 255:
                raise ValueError('binary threshold not in range [0, 255]')

            image_processor.binary_threshold(value)

        elif argument == 'reverse_colors':
            image_processor.reverse_colors()

        elif argument == 'rotate':
            image_processor.rotate(value)

        elif argument == 'cut':
            image_processor.cut(value)

# show images and wait for user input inside this method
image_processor.show_images()