import cv2
from os.path import join
from image_utils.image_processor import Image_Processor
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_raises

image_url = 'http://www.multientertainments.com/wp-content/uploads/2018/05/20180527143906-85.png'
test_images_dir = 'image_test'
    
    
class Test_image_download:
    def setUp(self):
        self.image_processor = Image_Processor()
        self.test_image = cv2.imread(join(test_images_dir, "poopy.png"))
    
    def test_init(self):
        assert(self.image_processor.original_image == None)
        assert(self.image_processor.processed_image == None)
        
    def test_downloading(self):
        self.image_processor.download_image(image_url)
        print('after downloading', self.image_processor.original_image)
        
        assert_array_almost_equal(self.image_processor.original_image,
                                      self.test_image)

def im_open(im_name):
    return cv2.imread(join(test_images_dir, im_name))

class Test_image_processing:
    def setUp(self):
        self.image_processor = Image_Processor()
        self.rotated_90 = im_open('rotated_90.png')
        self.rotated_180 = im_open('rotated_180.png')
        self.rotated_270 = im_open('rotated_270.png')
        self.gray = im_open('gray.png')[:, :, 0]
        self.image_processor.download_image(image_url)
        
    def test_rotate_90(self):
        self.image_processor.rotate(90)
        assert_array_equal(self.rotated_90,
                           self.image_processor.processed_image)
        
    def test_rotate_180(self):
        self.image_processor.rotate(180)
        assert_array_equal(self.rotated_180,
                           self.image_processor.processed_image)

    def test_rotate_270(self):
        self.image_processor.rotate(270)
        assert_array_equal(self.rotated_270,
                           self.image_processor.processed_image)
        
    def test_rotate_other(self):
        assert_raises(ValueError, self.image_processor.rotate, 24)
        
        
    def test_gray(self):
        self.image_processor.to_gray()
        assert_array_equal(self.gray, 
                           self.image_processor.processed_image)