import cv2
import numpy as np


image = cv2.imread("test.pgm", 0)
px = image[0, 0]
print px, "Thats how many channels there are"
flag = 0

print "image size", image.size



for x in range(1000):
    for y in range(1000):
        if(image[x,y] != 127):
            print x, y, "Coordinates of change"
            flag =1
if(flag==0):
    print "No luck, bruh"

