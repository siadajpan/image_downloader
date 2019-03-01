import cv2
import requests
from io import BytesIO
import numpy as np
import time


class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None

    # download image from url and save it to self.original_image
    def download_image(self, image_url):
        # convert content of request to byte stream
        img_stream = BytesIO(requests.get(image_url).content)
        # convert byte stream to string, and decode it as color (flag 1) image
        self.original_image = cv2.imdecode(np.fromstring(img_stream.read(), np.uint8), 1)

    # change color to gray scale
    def to_gray(self):

        self.processed_image = cv2.cvtColor(self.original_image,
                                            cv2.COLOR_BGR2GRAY)
        # merge into 3 channels picture, gray-scale picture
        # so it can be displayed with color one
        self.processed_image = cv2.cvtColor(self.processed_image,
                                            cv2.COLOR_GRAY2BGR)

    # rotate image by one of [90, 180, 270] degrees clockwise
    def rotate(self, rotation):
        # defy some flipping and transposing functions
        def h_flip(image):
            return cv2.flip(image, 1)

        def v_flip(image):
            return cv2.flip(image, 0)

        def transpose(image):
            return cv2.transpose(image)

        # process image depending on user choice
        if rotation == 90:
            self.processed_image = h_flip(transpose(self.original_image))

        elif rotation == 180:
            self.processed_image = h_flip(v_flip(self.original_image))

        elif rotation == 270:
            self.processed_image = v_flip(transpose(self.original_image))

        # raise exception if user specify different rotation
        else:
            raise ValueError('invalid rotation for image: ', rotation)

    # execute binary threshold
    def binary_threshold(self, threshold):
        if not 0 <= threshold <= 255:
            raise ValueError('binary threshold not in range [0, 255]')

        # first change the original image to gray scale
        self.to_gray()
        # execute binary threshold
        _, self.processed_image = cv2.threshold(self.processed_image,
                                                threshold, 255, cv2.THRESH_BINARY)

    # cut image into region specified by pixels
    def cut(self, pixels):
        # check if there is correct amount of values specified by user
        try:
            x_start, y_start, x_end, y_end = pixels
        except TypeError:
            raise TypeError('too many arguments for cut')
        except ValueError:
            raise TypeError('not enough arguments for cut')
        else:
            # get width and height of image and check if region is correct
            (height, width) = self.original_image.shape[:2]
            if not 0 <= x_start < x_end <= width or \
                    not 0 <= y_start < y_end <= height:
                raise ValueError('invalid parameters of cut x: {} y:{} to x: {}, y: {}\
                for image size width: {}, height: {}'.format(*pixels, width, height))
            self.processed_image = self.original_image[y_start: y_end, x_start: x_end]

    # reverse colors of an image using bitwise_not
    def reverse_colors(self):
        self.processed_image = cv2.bitwise_not(self.original_image)

    # private method to create image to display for user. Either original, or
    # original with processed side-by-side
    def _create_output_image(self):

        # show both images side-by-side if there is processed image
        if self.processed_image is not None:
            # calculate border size based on differences between heights
            height_o = self.original_image.shape[0]
            height_p = self.processed_image.shape[0]
            border = (max([height_o, height_p]) - min([height_o, height_p])) / 2

            # extend height of one of the images if heights are different
            if height_o > height_p:
                new_original = self.original_image
                new_processed = create_higher_image(self.processed_image, border)
            else:
                new_original = create_higher_image(self.original_image, border)
                new_processed = self.processed_image

            # concatenate pictures side-by-side
            out_image = np.concatenate((new_original, new_processed), axis=1)
            title = 'Image comparison'

        # output original image, if there was no processing
        else:
            out_image = self.original_image
            title = 'Original image'

        return [title, out_image]

    # display images and wait for user input
    def show_images(self):

        # create and display image
        title, image = self._create_output_image()
        cv2.imshow(title, image)

        # save pictures as user specify, quit after pressing 'q'
        while True:
            # wait for key press
            key_pressed = cv2.waitKey(0)

            # user pressed 'o'
            if key_pressed == ord('o'):
                self.save_original()

            # user pressed 'p' and there is a processed image
            elif key_pressed == ord('p') and self.processed_image is not None:
                self.save_processed()

            # user pressed 'b' and there is a processed image
            elif key_pressed == ord('b') and self.processed_image is not None:
                cv2.imwrite(create_file_name('_b'), image)

            # user pressed 'q'
            elif key_pressed == ord('q'):
                break

        cv2.destroyAllWindows()

    # save original image
    def save_original(self):
        file_name = create_file_name('_o')
        cv2.imwrite(file_name, self.original_image)
        # return filename for testing
        return file_name

    # save processed image
    def save_processed(self):
        file_name = create_file_name('_p')
        cv2.imwrite(file_name, self.processed_image)
        # return filename for testing
        return file_name


# static method for creating file names from current time and suffix
def create_file_name(suffix):
    ext = '.png'
    name = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + suffix + ext

    return name


# static method to add black boarders on top and below an image
def create_higher_image(image, border):
    # border is a float number. It can be either whole number (e.g. 4.0) or
    # whole number + 0.5 (e.g. 4.5). If it is whole, both int(border) and
    # int(border + 0.6) will return the same number (4). If the border is
    # e.g. 4.5, top border will be 4, and bottom will be int(5.1) = 5
    return cv2.copyMakeBorder(image, int(border), int(border + 0.6), 0, 0, cv2.BORDER_CONSTANT, 0)
