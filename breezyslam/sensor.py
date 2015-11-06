'''
sensor.py : Asus xtion which emulates a laser scaner
             
author: Nils Bernhardt 
'''

from breezyslam.components import Laser
from reader import Reader

import math





class XTION(Laser):

    viewangle = 58 #asus xtion view in degrees
    linecount = 2 #lines above and below to generate average (0=online desired line)
    distance_no_detection_mm = 10000 # todo find value
    scan_rate_hz = 10 #todo find value
    
    '''
    A class for the Asus XTION
    '''
    def __init__(self, log = True, detectionMargin = 0, offsetMillimeters = 0):
        self.log = log
        if(log):
            self.out = open('log', 'w')
        self.reader = Reader()
        self.width = self.reader.getHeight()
        self.height = self.reader.getWidth()
        self.row = self.height/2 #row to read
        Laser.__init__(self, self.width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm, detectionMargin, offsetMillimeters)
        
    

    '''
    Scans one line
    return: array with the values
    '''
    def scan(self):
        frame = self.reader.readFrame()
        data = self.readLine(frame, self.width, self.height, self.row)
        return data

        
    '''
    #Prints the depth value for every pixel in one line
    #frame_data - depth frame
    #width -  width of the frame
    #height - heigth of the frame
    #line - line to print
    return one data row converted as lidar
    '''
    def readLine(self, frame_data, width, height, line):
        data = []
        for x in range(width-1, -1, -1):
            value = self.getAverageDepth(frame_data, width, height, x, line, self.linecount)
            converted = self.toLidarValue(value, x, width)
            if(self.log):
                self.out.write(str(converted) + ' ')
            data.append(converted)
        if(self.log):
            self.out.write('\n')
        return data

    '''
    Converts the measured value of the asus xtion to the value a lidar would measure
    value: value to convert
    x: x position of the value
    width: of the frame
    return: converted value
    '''
    def toLidarValue(self, value, x, width):
        angle = (float(width)/2-x)/width*self.viewangle
        return int(value/math.cos(math.radians(angle)))

    '''
    #get the average value of a specifiv pixel with a certain amount of pixel above and under.
    #frame_data - depth frame
    #widht -  width of the frame
    #height - height of the frame
    #x - coordinate of the pixel
    #y - coordinate of the pixel
    return: average value
    '''
    #distance - amount of pixel under and above the desired position
    def getAverageDepth (self, frame_data, width, height, x, y, distance):
        value = 0;
        for xTemp in range (-distance+x, distance+1+x):
            value += frame_data[y*width+xTemp]
        return value/(distance+1);  
