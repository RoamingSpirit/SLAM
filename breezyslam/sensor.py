'''
sensor.py : Asus xtion which emulates a laser scaner
             
author: Nils Bernhardt 
'''

from breezyslam.components import Laser
from reader import Reader

import math





class XTION(Laser):

    viewangle = 58 #asus xtion view in degrees
    linecount = 5 #lines above and below to generate average (0=online desired line)
    distance_no_detection_mm = 3500 # max detection range
    scan_rate_hz = 23 #todo find value
    detectionMargin = 4 #pixels on the sites of the scans which should be ignored
    offsetMillimeters = 50 #offset of the sensor to the center of the robot
    
    '''
    A class for the Asus XTION
    '''
    def __init__(self, log = True):
        self.log = log
        if(log):
            self.out = open('log', 'w')
        self.reader = Reader()
        self.width = self.reader.getWidth()
        self.height = self.reader.getHeight()
        
        self.row = self.height/2 #row to read
        
        Laser.__init__(self, self.width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm, self.detectionMargin, self.offsetMillimeters)
        
    

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
    #distance - pixels under and above the desired row
    return: average value
    '''
    def getAverageDepth (self, frame_data, width, height, x, y, distance):
        sum = 0;
        count = 0
        for yTemp in range (-distance+y, distance+1+y):            
            value = frame_data[yTemp*width+x]
            if(value>0):
                sum += value
                count += 1
        if(count>0):
            return sum/count
        else:
            return 0

class FileXTION(XTION):
    #current frame read
    index = 100

    '''
    A class for reading the log file of an Asus XTION
    
    dataset: filename
    datadir: directionary of the file default '.'
    '''
    def __init__(self, dataset, datadir = '.'):
        self.scans, width = self.load_data(datadir, dataset)
        Laser.__init__(self, width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm, self.detectionMargin, self.offsetMillimeters)

    '''
    reads a scan 
    return: array with the values
    '''
    def scan(self):
        if(self.index < len(self.scans)):
           self.index += 1
           return self.scans[self.index-1]
        else:
           return []

    '''
    loads a stroed log file and saves the scans.
    datadir: directionary of the file
    dataset: filename
    return: scans, width of the scans
    '''
    def load_data(self, datadir, dataset):
        
        filename = '%s/%s' % (datadir, dataset)
        print('Loading data from %s...' % filename)
        
        fd = open(filename, 'rt')
        
        scans = []
        
        while True:  
            
            s = fd.readline()
            
            if len(s) == 0:
                break       
                
            toks = s.split()[0:-1] # ignore ''
                            
            lidar = [int(tok) for tok in toks[:]]

            for x in range(0, len(lidar)):
                if(lidar[x]>self.distance_no_detection_mm):
                    lidar[x]=0

            scans.append(lidar)
            
        fd.close()
            
        return scans, len(scans[0])
        
