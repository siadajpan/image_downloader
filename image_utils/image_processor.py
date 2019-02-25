import cv2
import requests

class Image_Processor:
    def __init__(self, im_url):
        self.image = download_image(im_url)
        
    def download_image(self, image_url):
        pass