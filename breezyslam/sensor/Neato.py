# -*- coding: utf-8 -*-
"""
Created on Wed Dec 02 12:13:15 2015

@author: Guillermo the Great
"""
from sensor import Sensor

import NeatoReader as nr
import math



class NEATO(Sensor):
    
    viewangle = 360 #Neato LiDAR view in degrees
    width = 360
    distance_no_detection_mm = 3500 # max detection range, ===========>>>>check to make sure its correct
    scan_rate_hz = 10 #todo find value
    detectionMargin = 0 #pixels on the sites of the scans which should be ignored
    offsetMillimeters = 50 #offset of the sensor to the center of the robot
    
    
    def __init__(self, log = True):
        self.log = log #Whether information should be saved in a log file
        #if(log):
         #   self.out = open('log', 'w')
        self.sensor = nr.NeatoReader()
        Sensor.__init__(self, self.width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm, self.detectionMargin, self.offsetMillimeters)
        
        

    def scan(self):
        data = self.sensor.scan()
        return data
       

    
