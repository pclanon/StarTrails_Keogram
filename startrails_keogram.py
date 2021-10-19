# startrails_keogram.py
# Make StarTrail and Keogram images from JPGs in last night's directory

import cv2 
import os 
import numpy
from fnmatch import fnmatch
from datetime import datetime, timedelta

os.system("logger 'Clanon startrails_keogram.py started.'")

y = datetime.now() - timedelta(1)
yesterday = datetime.strftime(y, '%Y%m%d')
# basepath = '/Users/paulclanon/Documents/Jupyter/Meteors/'
# basepath = '/Users/paulclanon/Documents/Jupyter/Meteors/temp/'
basepath = f'/media/allsky/allsky/images/{yesterday}/'
imagefiles = [name for name in os.listdir(basepath) if fnmatch(name, 'image*.jpg')]
imagefiles = sorted(imagefiles)
height, width = numpy.shape(cv2.imread(f'{basepath}{imagefiles[0]}'))[0:2]

stack   = numpy.zeros((height, width, 3), dtype = float)
keo = numpy.zeros((height, len(imagefiles), 3), dtype = float)
counter = 0

for imagefile in imagefiles:
    
    image_new = cv2.imread(f'{basepath}{imagefile}') #, dtype = float
    stack     = numpy.maximum(stack, image_new)
    keo[:, counter]   = image_new[:, int(width / 2)]
    counter  += 1

stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
keo = numpy.array(numpy.round(keo), dtype = numpy.uint8)

# star_trails = Image.fromarray(stack, mode = "RGB")
star_trails = stack #cv2.cvtColor(stack) #, cv2.COLOR_RGB2BGR
# keogram = Image.fromarray(keo, mode = "RGB")
keogram = keo #cv2.cvtColor(keo) #, cv2.COLOR_RGB2BGR

# Write times on keogram

keo_width = len(imagefiles)
first_image_time = datetime.strptime(imagefiles[0][6:20], '%Y%m%d%H%M%S')  
first_image_at = datetime.strftime(first_image_time, '%-I:%M%p') #%b %d, %Y\n %H:%M:%S
first_image_date = datetime.strftime(first_image_time, '%b %d, %Y')
last_image_time = datetime.strptime(imagefiles[-1][6:20], '%Y%m%d%H%M%S')  
last_image_at = datetime.strftime(last_image_time, '%-I:%M%p') #%b %d, %Y\n

# Text on keogram
    
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# origin points on image (width = # of images, height = 2028)
orig_upper_left = (25, 100) # (w, h)
orig_super_top_center = (375, 75)
orig_top_center = (400, 110)
orig_sub_top_center = (400, 145)
orig_upper_right = (770, 100)
orig_bottom_left = (25, 1420)

# fontScale
fontScale = 1

# Black color in BGR
color = (0, 0, 0)

# Line thickness in px
thickness = 2

# Using cv2.putText() method

keogram = cv2.putText(keogram, 'San Francisco, CA', orig_super_top_center, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
keogram = cv2.putText(keogram, f'{first_image_at} --->', orig_upper_left, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
keogram = cv2.putText(keogram, first_image_date, orig_top_center, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
keogram = cv2.putText(keogram, 'pac@well.com', orig_sub_top_center, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
keogram = cv2.putText(keogram, f' ---> {last_image_at}', orig_upper_right, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
keogram = cv2.putText(keogram, f'{keo_width} Images, 30-sec Exposures', orig_bottom_left, font, 
                   fontScale, color, thickness, cv2.LINE_AA)

# Add hour ticks to keogram

hours_in_filenames = [a[14:16] for a in imagefiles] 
hour_ticks = list(dict.fromkeys(hours_in_filenames))[1:-1] 
hour_ticks = [f'{a}h' for a in hour_ticks]
minutes_to_first_tick = 60-first_image_time.minute

minutes_in_keogram = (last_image_time - first_image_time).total_seconds() / 60
pixels_per_minute = len(imagefiles)/minutes_in_keogram

column_of_first_tick = int(pixels_per_minute * minutes_to_first_tick)
columns_between_ticks = int(60 * pixels_per_minute)

counter=0

for t in hour_ticks:
    keogram = cv2.putText(keogram, t, (column_of_first_tick+(columns_between_ticks*counter), 225), 
                          font, fontScale, color, thickness, cv2.LINE_AA)
    counter +=1

# Text on Startrails
    
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# origin points on image (size = 2028,1520)
orig_upper_left = (50, 100)
orig_bottom_right = (1750, 1420)
orig_upper_right = (1550, 100)
orig_bottom_left = (150, 1420)

# fontScale
fontScale = 1

# White-ish color in BGR
color = (144, 222, 255)

# Line thickness of 2 px
thickness = 2

# Using cv2.putText() method
star_trails = cv2.putText(star_trails, '30-Second Exposures', orig_upper_left, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
star_trails = cv2.putText(star_trails, 'pac@well.com', orig_bottom_right, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
star_trails = cv2.putText(star_trails, 'Raspberry Pi HQ Camera', orig_upper_right, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
star_trails = cv2.putText(star_trails, 'Paul Clanon', orig_bottom_left, font, 
                   fontScale, color, thickness, cv2.LINE_AA)

# Save to disk

# cv2.imwrite(f'{basepath}stacked_image_{yesterday}.jpg', star_trails)
# cv2.imwrite(f'{basepath}keogram_{yesterday}.jpg', keogram)
cv2.imwrite(f'/media/allsky/allsky/stackedtrails/stacked_image_{yesterday}.jpg', star_trails)
cv2.imwrite(f'/media/allsky/allsky/keograms/keogram_{yesterday}.jpg', keogram)

# cv2.imwrite(f'{basepath}stacked_image_20211013.jpg', star_trails)
# cv2.imwrite(f'{basepath}keogram_20211013.jpg', keogram)

os.system("logger 'Clanon startrails_keogram.py completed. Launching starmap5.py'")

# Launch starmap5.py

os.system('python3 ~/starmap5.py')
