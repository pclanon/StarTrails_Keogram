# Make StarTrail image from JPGs in last night's directory

import os 
import numpy as np
from fnmatch import fnmatch
from PIL import Image
from datetime import datetime, timedelta

y = datetime.now() - timedelta(1)
yesterday = datetime.strftime(y, '%Y%m%d')
basepath = '/Users/paulclanon/Documents/Jupyter/Meteors/cloudy/'
# basepath = ''.join('/media/allsky/allsky/images/' + yesterday + '/')
imagefiles = [name for name in os.listdir(basepath) if fnmatch(name, 'image*.jpg')]
width, height = Image.open(''.join(basepath + imagefiles[0])).size
stack   = np.zeros((height, width, 3), dtype = float)
counter = 1
threshold = .1 # Circle is 58% of whole image

for imagefile in imagefiles:
    
    image_new = np.array(Image.open(''.join(basepath + imagefile)), dtype = float)
    
    if ((np.count_nonzero(image_new > [200, 200, 200])) / (width * height)) < threshold:
        stack = np.maximum(stack, image_new)
        print (f'{counter} under threshold')
        counter += 1
        
    else:
        pass

stack = np.array(np.round(stack), dtype = np.uint8)
output = Image.fromarray(stack, mode = "RGB")
output.save(f'{basepath}stacked_image_{yesterday}.jpg', "JPEG")
# output.save(f'/media/allsky/allsky/stackedtrails/stacked_image_{yesterday}.jpg', "JPEG")
