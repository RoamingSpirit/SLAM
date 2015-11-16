# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

import sys
sys.path.insert(0, '/home/pi/libardrone/python-ardrone')
import libardrone
import cv2
import time
import threading
import math
from vehicle import Vehicle

class Drone(Vehicle, threading.Thread):
    """
    Class representing a connection to the ARDrone,
    controls it and receive navdata information
    """
    running = True
    correct_psi = True
    old_timestamp = 0.0

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

    def get_dt(self):
        """
        Return the time difference between since the last update
        """
        now = time.time()
        if self.old_timestamp == 0.0:
            self.old_timestamp = now
            return 0.0
        dt = now-self.old_timestamp
        self.old_timestamp = now
        return dt

    def calc_distance(self, vx, dt):
        """
        Calculate distance since last frame
        """
        return vx*dt

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
        dt = self.get_dt()
        dthata = self.calc_dthata(self.drone.navdata.get(0, dict()).get('psi', 0))
        if self.correct_psi & (math.fabs(dthata) > 20):
                dthata = 0
                self.correct_psi = False
        return self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0), dt), dthata, dt
        
    def initialize(self):
        """
        Lets the drone fly
        """
        print "Take off"
        #self.drone.takeoff()
	print "Drone in air!"

    def shutdown(self):
        """
        Close application
        """
        print "Shutting down..."
        #self.drone.land()
        self.cam.release()
        self.running = False
        self.drone.halt()
        print "Drone shutted down."
