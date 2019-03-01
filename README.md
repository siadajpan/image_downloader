# Image downloader project

Application should download a picture specified by user, using URL path. User should be able to specify one postprocessing executed on the downloaded picture. User should be presented with the original and postprocessed pictures, and be able to save one or both of those pictures.

## Requirements
User should create virtual environment using `venv`, python 3 (created on python=3.6.5) and requirements from `requirements.txt`

## Execution
 Program should be executed on console as described below:
```
python image_downloader.py image_url option [parameters]
```
where:
* `image_url` - string based url for picture 
* `option [parameters]` - one of the postprocessing options specified below

### Postprocessing options
* `-g` change color image into grayscale
```
python http://<path_to_pic>.png -g
```
* `-b THRESHOLD` execute binary threshold where `THRESHOLD` is integer parameter value 0 - 255
```
python http://<path_to_pic>.png -b 100
```
* `-rc` reverse colors
```
python http://<path_to_pic>.png -rc
```
* `-r ANGLE` rotate picture clockwise by angle where `ANGLE` is parameter from [90, 180, 270]
```
python http://<path_to_pic>.png -r 180
```
* `-c PIXELS` cut image specifyed by `PIXELS` as 4 coordinates: x_start y_start x_end y_end **with no comma** (coordinates x_start: 0 and y_start: 0 being top left of the picture)
```
python http://<path_to_pic>.png -c 10 20 250 400
```
* no option will just display original picture
```
python http://<path_to_pic>.png
```
	
## Output
User should be presented with original image, and - in case of processing - processed image.
User then has an option to save images by pressing one of the buttons which will save the image in .png format with name of current date and time:
* `o` will save the original image with suffix `_o`
* `p` will save the processed image `_p`
* `b` will save both the original image and processed image with suffix `_b`
* `q` will quit the program

## Testing
To execute test user should use command below:
```
nosetests test_image_processor.py
```
