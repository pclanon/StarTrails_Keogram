# startrails_keogram5.py

# create  all/slice modes to make time ranges easier
# adding animated startrail
# Add option to specify time range, to zero in

import cv2 
import os 
import numpy
from fnmatch import fnmatch
from datetime import datetime, timedelta

os.system("logger 'Clanon startrails_keogram5.py started.'")

# Function to put text on Startrails images and animation

def text_on_startrails(image_name, mode):
    
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # origin points on image (size = 2028,1520)
    orig_upper_left = (50, 100)
    orig_upper_left_sub1 = (50, 135)
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
    image_name = cv2.putText(image_name, '30-Second Exposures', orig_upper_left, font, 
                       fontScale, color, thickness, cv2.LINE_AA)
    if mode == 'animated':
        image_name = cv2.putText(image_name, imagefile[6:20], orig_upper_left_sub1, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
    image_name = cv2.putText(image_name, 'pac@well.com', orig_bottom_right, font, 
                       fontScale, color, thickness, cv2.LINE_AA)
    image_name = cv2.putText(image_name, 'Raspberry Pi HQ Camera', orig_upper_right, font, 
                       fontScale, color, thickness, cv2.LINE_AA)
    image_name = cv2.putText(image_name, 'Paul Clanon', orig_bottom_left, font, 
                       fontScale, color, thickness, cv2.LINE_AA)

mode = 'all' # 'all' or 'slice'
start_stop_times = [(20211230020000, 20211230077500),]
y = datetime.now() - timedelta(1)
yesterday = datetime.strftime(y, '%Y%m%d')
# basepath = '/Users/paulclanon/Documents/Jupyter/Meteors/'
# basepath = '/Users/paulclanon/Documents/Jupyter/Meteors/temp/'
basepath = f'/media/allsky/allsky/images/{yesterday}/'
imagefiles = [name for name in os.listdir(basepath) if fnmatch(name, 'image*.jpg')]
imagefiles = sorted(imagefiles)

# Option to specify a time range for images, e.g. make a startrail during clear stretch
if mode == 'slice':
    time_slice = []
    for slice in start_stop_times:
        for image in imagefiles:
            if (int(image[6:20]) >= slice[0] and int(image[6:20]) <= slice[1]):
                time_slice.append(image)

    imagefiles = time_slice

height, width = numpy.shape(cv2.imread(f'{basepath}{imagefiles[0]}'))[0:2]
size = (width, height)

stack   = numpy.zeros((height, width, 3), dtype = float)
keo = numpy.zeros((height, len(imagefiles), 3), dtype = float) # (adjust width for # of pixels)
counter = 0

# Set up animated startrails movie to write to

fourcc = cv2.VideoWriter_fourcc(*'h264')
if mode == 'slice':
    vvw = cv2.VideoWriter(f'/media/allsky/allsky/stackedtrails/{yesterday}_sliced_animated_startrails.mp4', 
                      fourcc, 20, size, isColor=True)
else:
    vvw = cv2.VideoWriter(f'/media/allsky/allsky/stackedtrails/{yesterday}_animated_startrails.mp4', 
                      fourcc, 20, size, isColor=True)

for imagefile in imagefiles:
    
    image_new = cv2.imread(f'{basepath}{imagefile}') 
    stack     = numpy.maximum(stack, image_new)
    stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
    anim_stack = numpy.copy(stack)
    text_on_startrails(anim_stack, 'animated')
    vvw.write(anim_stack)
    #text_on_startrails(stack, 'animated')
    #vvw.write(stack)
    keo[:, counter]   = image_new[:, int(width / 2)]
    counter  += 1

# Use this for keograms with multiple-pixel slices
#pixel_swath = 13 #must be odd number to keep centered
#keo = numpy.zeros((height, pixel_swath, 3), dtype = float)

#for p in range(0, pixel_swath):
#    keo[:, p]   = image_new[:, int(width / 2)-int((pixel_swath-1)/2)+p] 
vvw.release()
stack = numpy.array(numpy.round(stack), dtype = numpy.uint8)
keo = numpy.array(numpy.round(keo), dtype = numpy.uint8)

star_trails = stack 
keogram = keo 

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
orig_super_top_center = (int(keo_width/2)-160, 75) 
orig_top_center = (int(keo_width/2)-120, 110) 
orig_sub_top_center = (int(keo_width/2)-125, 145) 
orig_upper_right = (keo_width-270, 100) # 270 ~ 14 characters
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

# Text on Startrails Still Image

text_on_startrails(star_trails, 'still')


# Save to disk

if mode == 'slice':
    cv2.imwrite(f'/media/allsky/allsky/stackedtrails/{yesterday}_sliced_stacked_image.jpg', star_trails)
else:
    cv2.imwrite(f'/media/allsky/allsky/stackedtrails/{yesterday}_stacked_image.jpg', star_trails)

if mode == 'all':
    cv2.imwrite(f'/media/allsky/allsky/keograms/{yesterday}_keogram.jpg', keogram)

# Log end

if mode == 'all':
    os.system("logger 'Clanon startrails_keogram5.py completed. Launching starmap6.py'")
if mode == 'slice':
    os.system("logger 'Clanon startrails_keogram5.py completed in slice mode'")

# Launch starmap6.py

if mode == 'all':
    os.system('python3 ~/starmap6.py')
