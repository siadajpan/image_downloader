import cv2
from os.path import join
from image_utils.image_processor import Image_Processor
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_raises
import time 
import os

image_url = 'http://www.multientertainments.com/wp-content/uploads/2018/05/20180527143906-85.png'
test_images_dir = 'image_test'

def im_open(im_name):
    return cv2.imread(join(test_images_dir, im_name))

    
# test downloading image using url path
class Test_image_download:
    # initiliaze our class object
    def setup(self):
        self.image_processor = Image_Processor()
        
    # at the beginning both images should be set to None
    def test_init(self):
        assert(self.image_processor.original_image == None)
        assert(self.image_processor.processed_image == None)
    
    # test downloading the image, compare it to the image saved previously
    def test_downloading(self):
        self.image_processor.download_image(image_url)
        assert_array_almost_equal(im_open("poopy.png"),
                                  self.image_processor.original_image)

# test image processing methods
class Test_image_processing:
    # initialize object and download the image. Set paths of saved files to None
    def setup(self):
        self.image_processor = Image_Processor()
        self.image_processor.download_image(image_url)
        self.saved_original = None
        self.saved_processed = None
        
    # after testing saving, remove saved pictures
    def teardown(self):
        if self.saved_original:
            os.remove(self.saved_original)
        if self.saved_processed:    
            os.remove(self.saved_processed)
        
    # test rotation by 90
    def test_rotate_90(self):
        self.image_processor.rotate(90)
        assert_array_equal(im_open('rotated_90.png'),
                           self.image_processor.processed_image)
        
    # test rotation by 180    
    def test_rotate_180(self):
        self.image_processor.rotate(180)
        assert_array_equal(im_open('rotated_180.png'),
                           self.image_processor.processed_image)

    # test rotation by 270
    def test_rotate_270(self):
        self.image_processor.rotate(270)
        assert_array_equal(im_open('rotated_270.png'),
                           self.image_processor.processed_image)
    
    # check if rotation by other value than 90, 180 or 270 raises exception
    def test_rotate_other(self):
        assert_raises(ValueError, self.image_processor.rotate, 24)
        
    # test changing to gray scale
    def test_gray(self):
        self.image_processor.to_gray()
        assert_array_equal(im_open('gray.png'), 
                           self.image_processor.processed_image)
        
    # test binary threshold
    def test_binary(self):
        self.image_processor.binary_threshold(100)
        assert_array_equal(im_open('binary100.png'),
                           self.image_processor.processed_image)
    
    # test if after setting binary threshold to wrong value, exception is raised
    def test_binary_wrong_value(self):
        assert_raises(ValueError, self.image_processor.binary_threshold, -6)
        assert_raises(ValueError, self.image_processor.binary_threshold, 300)
    
    # test if setting invalid number to cutting, exception is raised
    def test_invalid_cut(self):
        assert_raises(ValueError, self.image_processor.cut, (-6, 14, 24, 300))
        assert_raises(ValueError, self.image_processor.cut, (50, 14, 24, 300))
        assert_raises(ValueError, self.image_processor.cut, (25, 453, 24, 300))
        assert_raises(ValueError, self.image_processor.cut, (50, 140, 24, 30))
        assert_raises(ValueError, self.image_processor.cut, (50, 14000, 24, 14200))
        assert_raises(ValueError, self.image_processor.cut, (50, 14000, -24, 40))
        
    # test if setting invalid amount of parameters in cutting, raises exception
    def test_invalid_number_of_arguments_cut(self):
        assert_raises(TypeError, self.image_processor.cut, (2, 5, 30))
        assert_raises(TypeError, self.image_processor.cut, (2, 5, 30, 20, 35))

    # test cutting part of picture
    def test_cut(self):
        self.image_processor.cut((310, 3, 410, 138))
        assert_array_equal(im_open('cut.png'),
                           self.image_processor.processed_image)
    
    # test reversing colors
    def test_reverse_colors(self):
        self.image_processor.reverse_colors()
        assert_array_equal(im_open('reversed.png'),
                           self.image_processor.processed_image)

    # test saving original picture
    def test_save_original(self):
        self.saved_original = self.image_processor.save_original()
        # wait 1 second until image is saved
        time.sleep(1)
        image = cv2.imread(self.saved_original)
        assert_array_equal(self.image_processor.original_image, image)
        
    # test saving processed picture    
    def test_save_processed(self):
        self.image_processor.cut((310, 3, 410, 138))
        self.saved_processed = self.image_processor.save_processed()
        # wait 1 second until image is saved
        time.sleep(1)
        image = cv2.imread(self.saved_processed)
        assert_array_equal(self.image_processor.processed_image, image)