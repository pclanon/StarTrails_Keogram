# startrails_keogram3.py
# Add option to specify time range, to zero in
# This revision -- tie keogram text origin points to varying size of image (charwidth~20px)
# This revision -- add number_of_pixels variable, use in initializing keo array and
#           in a for loop in the actual slicing step
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

# Option to specify a time range for images, e.g. make a startrail during clear stretch
#start_image = 20211107010000
#stop_image = 20211107050000
#time_slice = [image for image in imagefiles if 
#              (int(image[6:20]) >= start_image and int(image[6:20]) <= stop_image)]
#imagefiles = time_slice

height, width = numpy.shape(cv2.imread(f'{basepath}{imagefiles[0]}'))[0:2]

stack   = numpy.zeros((height, width, 3), dtype = float)
#keo = numpy.zeros((height, len(imagefiles), 3), dtype = float) # (adjust width for # of pixels)
#counter = 0
filter_threshold = 45

for imagefile in imagefiles:
    
    image_new = cv2.imread(f'{basepath}{imagefile}')
    if numpy.average(image_new) >  filter_threshold:
        continue 
    stack     = numpy.maximum(stack, image_new)
    #keo[:, counter]   = image_new[:, int(width / 2)]
    #counter  += 1

# Use this for keograms with multiple-pixel slices
#pixel_swath = 13 #must be odd number to keep centered
#keo = numpy.zeros((height, pixel_swath, 3), dtype = float)

#for p in range(0, pixel_swath):
#    keo[:, p]   = image_new[:, int(width / 2)-int((pixel_swath-1)/2)+p] 

stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
#keo = numpy.array(numpy.round(keo), dtype = numpy.uint8)

star_trails = stack 
#keogram = keo 

# Write times on keogram

#keo_width = len(imagefiles)
#first_image_time = datetime.strptime(imagefiles[0][6:20], '%Y%m%d%H%M%S')  
#first_image_at = datetime.strftime(first_image_time, '%-I:%M%p') #%b %d, %Y\n %H:%M:%S
#first_image_date = datetime.strftime(first_image_time, '%b %d, %Y')
#last_image_time = datetime.strptime(imagefiles[-1][6:20], '%Y%m%d%H%M%S')  
#last_image_at = datetime.strftime(last_image_time, '%-I:%M%p') #%b %d, %Y\n

# Text on keogram
    
# font
#font = cv2.FONT_HERSHEY_SIMPLEX

# origin points on image (width = # of images, height = 2028)
#orig_upper_left = (25, 100) # (w, h)
#orig_super_top_center = (int(keo_width/2)-160, 75) 
#orig_top_center = (int(keo_width/2)-120, 110) 
#orig_sub_top_center = (int(keo_width/2)-125, 145) 
#orig_upper_right = (keo_width-270, 100) # 270 ~ 14 characters
#orig_bottom_left = (25, 1420)

# fontScale
#fontScale = 1

# Black color in BGR
#color = (0, 0, 0)

# Line thickness in px
#thickness = 2

# Using cv2.putText() method

#keogram = cv2.putText(keogram, 'San Francisco, CA', orig_super_top_center, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)
#keogram = cv2.putText(keogram, f'{first_image_at} --->', orig_upper_left, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)
#keogram = cv2.putText(keogram, first_image_date, orig_top_center, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)
#keogram = cv2.putText(keogram, 'pac@well.com', orig_sub_top_center, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)
#keogram = cv2.putText(keogram, f' ---> {last_image_at}', orig_upper_right, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)
#keogram = cv2.putText(keogram, f'{keo_width} Images, 30-sec Exposures', orig_bottom_left, font, 
 #                  fontScale, color, thickness, cv2.LINE_AA)

# Add hour ticks to keogram

#hours_in_filenames = [a[14:16] for a in imagefiles] 
#hour_ticks = list(dict.fromkeys(hours_in_filenames))[1:-1] 
#hour_ticks = [f'{a}h' for a in hour_ticks]
#minutes_to_first_tick = 60-first_image_time.minute

#minutes_in_keogram = (last_image_time - first_image_time).total_seconds() / 60
#pixels_per_minute = len(imagefiles)/minutes_in_keogram

#column_of_first_tick = int(pixels_per_minute * minutes_to_first_tick)
#columns_between_ticks = int(60 * pixels_per_minute)

#counter=0

#for t in hour_ticks:
 #   keogram = cv2.putText(keogram, t, (column_of_first_tick+(columns_between_ticks*counter), 225), 
  #                        font, fontScale, color, thickness, cv2.LINE_AA)
   # counter +=1

# Text on Startrails
    
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# origin points on image (size = 2028,1520)
orig_upper_left = (50, 100)
orig_upper_left_filter = (50, 140)
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
star_trails = cv2.putText(star_trails, f'Cloud Filter On: {filter_threshold}', orig_upper_left_filter, font, 
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
cv2.imwrite(f'/media/allsky/allsky/stackedtrails/{yesterday}_stacked_image_filter_on.jpg', star_trails)
#cv2.imwrite(f'/media/allsky/allsky/stackedtrails/{yesterday}_stacked_image_{start_image}.jpg', star_trails)
#cv2.imwrite(f'/media/allsky/allsky/keograms/{yesterday}_keogram.jpg', keogram)

# cv2.imwrite(f'{basepath}stacked_image_20211013.jpg', star_trails)
# cv2.imwrite(f'{basepath}keogram_20211013.jpg', keogram)

os.system("logger 'Clanon startrails_keogram.py completed. Launching starmap5.py'")

# Launch starmap5.py

#os.system('python3 ~/starmap5.py')
