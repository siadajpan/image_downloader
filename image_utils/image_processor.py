import cv2
import requests
from PIL import Image
from io import BytesIO
import numpy as np

class Image_Processor:
    def __init__(self):
        self.original_image = None
        self.processed_image = None
        
    def download_image(self, image_url):
        img_stream = BytesIO(requests.get(image_url).content)
        self.original_image = cv2.imdecode(np.fromstring(img_stream.read(), 
                                                         np.uint8), 1)
        
    def to_gray(self):
        self.processed_image = cv2.cvtColor(self.original_image, 
                                            cv2.COLOR_BGR2GRAY)
    
    def rotate(self, rotation):
        
        def h_flip(image):
            return cv2.flip(image, 1)
        
        def v_flip(image):
            return cv2.flip(image, 0)
        
        def transpose(image):
            return cv2.transpose(image)
        
        if rotation == 90:
            self.processed_image = h_flip(transpose(self.original_image))
            
        elif rotation == 180:
            self.processed_image = h_flip(v_flip(self.original_image))
            
        elif rotation == 270:
            self.processed_image = v_flip(transpose(self.original_image))
            
        else:
            raise ValueError('invalid rotation for image: ', rotation)
    
    def binary_threshold(self, threshold):
        pass
    
    def cut(self, pixels):
        pass
    
    def reverse_colors(self):
        pass
    
    def show_images(self):
        pass