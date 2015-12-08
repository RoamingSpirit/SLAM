# -*- coding: utf-8 -*-
"""
Created on Fri Dec 04 13:19:34 2015

@author: Guillermo the Great
"""

import serial

import sys
import signal



class NeatoReader:
    
    def __init__(self, log = True):
        Baudrate = 115200 #comminication speed
        COMport = '/dev/ttyACM0' # check to see devices to see where it is connected
        
        self.neatoSerial = serial.Serial(COMport, Baudrate)
        self.scan = self.scan #add the method
        self.message = "ShowDist\n" #used to get usable information from lidar. Send this message before receiving from lidar

        self.log = log
        if(log):
            self.out = open('logNeato', 'w')
        
        """
        read_scan
        returns an array of ints, corresponding to 360 distance readings from angle
        0 to 359, in order        
        """
    def scan(self):
        #The variables
        tempBuffer = [] #buffer for taking in stream of serial data        
        intArray = [] #we return this
        startFlag = 0 #When we find the start sequence, this is triggered
        endRead = 0 #set to 1 to kill the program
        #THe magic
        print "Beginning Serial Communication"
        self.neatoSerial.write(self.message) #Begin to get good information type
        
        while len(intArray) != 1:
            
            if self.neatoSerial.inWaiting() > 0: #Check to see if any pending messages from lidar
                inByte = self.neatoSerial.readline() #reads up to the end-of-line \r\n and stores it
                
                if startFlag == 0: #Find the start of the stream
                    try:
                        index = inByte.split(' ', 3)[0]
                        if index == '0:':                
                            startFlag = 1
                    except IndexError: #sometimes we get lines with garbage. Just skip them and get new data
                        pass
    
                if startFlag == 1: #collect the stream
                    tempBuffer.append(inByte)
                    
            if len(tempBuffer) == 360:
                
                for x in tempBuffer:
                    if len(x.split()) > 1:
                        try:
                            #We split the string into 3, and return the middle (which is the distance)
                            toks = x.split(' ', 3)
                            value = toks[1]
                            if(self.log):
                                self.out.write(value + ' ')
                            #intArray.append(int(value))
    
                        except IndexError, ValueError:
                            #self.neatoSerial.close()
                            print "Data recorded was weird. Look, data is: ", x
                            break
                endRead = 1
                if(self.log):
                    self.out.write('\n')
                print "ending"
                return intArray
            #self.neatoSerial.close()
                

            
