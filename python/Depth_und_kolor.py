# -*- coding: utf-8 -*-
"""ff
Created on Wed Nov 04 13:30:07 2015

@author: Guillermo the Great
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 17:19:51 2015

@author: Guillermo the Great
"""

'''
Short test file, may get longer
'''
#from primesense import openni2
#from primesense import _openni2 as c_api
#numpy, for matrix manipulation fo the images
#import numpy as np
#matplotlib, for temporary display to check the images
#import matplotlib.pyplot as plt
#NOTE: Matplotlib will not display depth correctly: uint16 is made into uint8, so overflow cause stripes

'''
Starter test program
'''

from primesense import openni2
from primesense import _openni2 as c_api
import numpy as np
#import matplotlib.pyplot as plt
#alternate to matplotlib:
import cv2 #opencv, which uses numpy arrays for images anyway: can handle uint16 depth







path = '/home/pi/devel/OpenNI2/Packaging/OpenNI-Linux-Arm-2.2/Redist'

#author Nils
#Prints the depth value for every pixel in one line
#frame_data - depth frame
#width -  width of the frame
#height - heigth of the frame
#line - line to print
def print_line (frame_data, width, height, line):
    print "new frame"
    for x in range(0,width):
        print getAverageDepth(frame_data, width, height, x, line, 4)

#author Nils
#get the average value of a specifiv pixel with a certain amount of pixel above and under.
#frame_data - depth frame
#widht -  width of the frame
#height - height of the frame
#x - coordinate of the pixel
#y - coordinate of the pixel
#distance - amount of pixel under and above the desired position
def getAverageDepth (frame_data, width, height, x, y, distance):
    value = 0;
    for xTemp in range (-distance+x, distance+1+x):
        value += frame_data[y*width+xTemp]
    return value/(distance+1);


#takes frame data, and the type it is and displays the image
#frame_data = frame.get_buffer_as_blah(); thisType = numpy.someType
def print_frame(frame_data, thisType):
    #need to know what format to get the buffer in:
    # if color pixel type is RGB888, then it must be uint8, 
    #otherwise it will split the pixels incorrectly
    img  = np.frombuffer(frame_data, dtype=thisType)
    whatisit = img.size
    #QVGA is what my camera defaulted to, so: 1 x 240 x 320
    #also order was weird (1, 240, 320) not (320, 240, 1)
    if whatisit == (320*240*1):#QVGA
        #shape it accordingly, that is, 1048576=1024*1024
        img.shape = (1, 240, 320)#small chance these may be reversed in certain apis...This order? Really?
        #filling rgb channels with duplicates so matplotlib can draw it (expects rgb)
        img = np.concatenate((img, img, img), axis=0)
        #because the order is so weird, rearrange it (third dimension must be 3 or 4)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (320*240*3):
        #color is miraculously in this order
        img.shape = (240, 320, 3)
    else:
        print "Frames are of size: ",img.size

    #images still appear to be reflected, but I don't need them to be correct in that way
    print img.shape
    #need both of follwoing: plt.imShow adds image to plot
    #plt.imshow(img)
    #plt.show shows all the currently added figures
    #plt.show()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5,5), 0)
    cv2.imshow("im", image)

    
    #flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    canny = cv2.Canny(image, 30, 150)
    cv2.imshow("Original", canny)
    canny = cv2.Canny(image, 30, 50)
    cv2.imshow("Less,", canny)
    #if(cv2.waitKey(100) & 0xFF == ord('q')):
        #cv2.destroyAllWindows()
        
        
        
openni2.initialize(path)     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()
print dev.get_sensor_info(openni2.SENSOR_DEPTH)

depth_stream = dev.create_depth_stream()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 320, resolutionY = 240, fps = 30))
depth_stream.start()

color_stream = dev.create_color_stream()
color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 320, resolutionY = 240, fps = 30))
color_stream.start()

flagy = 1
while(flagy == 1):
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
   
    Color_frame = color_stream.read_frame()
    frame_data1 = Color_frame.get_buffer_as_uint8()

    print_line(frame_data1, 320, 240, 160)
    
    #print_frame(frame_data1, np.uint8)
    #print_frame(frame_data, np.uint16)
    if(cv2.waitKey(10) & 0xFF == ord('q')):
        cv2.destroyAllWindows()
        break
    
    
depth_stream.stop()

#depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 320, resolutionY = 240, fps = 30))
#depth_stream.start()
#frame = depth_stream.read_frame()
#frame_data = frame.get_buffer_as_uint16()
#print_frame(frame_data, np.uint16)
#depth_stream.stop()


#print "Testing Color "
#color_stream = dev.create_color_stream()
#color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 320, resolutionY = 240, fps = 30))
#color_stream.start()
#while(flagy == 1):
#    
#    frame = color_stream.read_frame()
#    frame_data1 = frame.get_buffer_as_uint8()
#    print_frame(frame_data1, np.uint8)
#    if(cv2.waitKey(100) & 0xFF == ord('q')):
#        cv2.destroyAllWindows()
#        break
color_stream.stop()


print "Leaving"
openni2.unload()
