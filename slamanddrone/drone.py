# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

import libardrone
import cv2
import time
from vehicle import Vehicle
import threading

class Drone(Vehicle,threading.Thread):
    """
    Class representing a connection to the ARDrone, controls it and receive navdata information
    """
    running = True
    UNHANDED_UPDATES = 10
    update_count = 0
    timestamp_frame = 0.0
    timestamp_update = 0.0

    def __init__(self):
        """
        Initialize the connection and variables
        """
        threading.Thread.__init__(self)
        print "Connecting..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        self.last_thata = self.drone.navdata.get(0, dict()).get('psi', 0)
        #cv2.namedWindow('Front camera')
    
    def get_dt_frame(self):
        """
        Return the time difference between since the last frame
        """
        dt,self.timestamp_frame=self.calc_dt(self.timestamp_frame)
        return dt
    
    def get_dt_update(self):
        """
        Return the time difference between since the last update
        """
        dt,self.timestamp_update=self.calc_dt(self.timestamp_update)
        return dt

    def calc_dt(self,old):
        """
        Return the time difference between old time and now
        """
        now = time.time()
        if old == 0.0:
            return 0.0,now
        dt = now-old
        return dt, now
        
    def calc_distance(self, vx):
        """
        Calculate distance since last frame
        """
        return vx*self.get_dt_frame()
            
    def calc_dthata(self, thata):
        """
        Calculate dthata since last call
        """
        dthata = thata - self.last_thata
        self.last_thata = thata
        return dthata
        
    def getOdometry(self):
        """
        return a tuple of odometry (dxy in mm,dthata in degree, dt in s)
        """
        if self.update_count == 0:
            self.update_count += 1
            return 0.0,0,self.get_dt_update()
	elif self.update_count < self.UNHANDED_UPDATES:
	    self.update_count += 1
            return 0.0,0,self.get_dt_update()	
        return self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0)),self.calc_dthata(self.drone.navdata.get(0, dict()).get('psi', 0)),self.get_dt_update()
        
    def initialize(self):
        """
        Lets the drone fly
        """
        print "Take off"
        #drone.takeoff()
	print "Drone in air!"

    def shutdown(self):
        """
        Close application
        """
        print "Shutting down..."
        self.cam.release()
        self.running = False
        self.drone.halt()
        print "Drone shutted down."
