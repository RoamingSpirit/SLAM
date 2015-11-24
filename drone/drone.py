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
import math

DRONE_SPEED = 0.1
TESTING = True

class Drone():
    '''
    Class representing a connection to the ARDrone,
    controls it and receive navdata information
    '''
    correct_psi = True
    in_air = False
    moving = False
    turning = False
    cmd = 0
    old_timestamp = 0.0

    def __init__(self, log = True):
        '''
        Initialize the connection and variables
        '''
        self.log = log
        if(log):
            self.out = open('odometry', 'w')
        print "Connecting..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        self.last_thata = self.drone.navdata.get(0, dict()).get('psi', 0)

    def get_dt(self):
        '''
        Return the time difference between since the last update
        '''
        now = time.time()
        if self.old_timestamp == 0.0:
            self.old_timestamp = now
            return 0.0
        dt = now-self.old_timestamp
        self.old_timestamp = now
        return dt

    def calc_distance(self, vx, dt):
        '''
        Calculate distance since last frame
        '''
        return vx*dt

    def calc_dthata(self, thata):
        '''
        Calculate dthata since last call
        '''
        dthata = thata - self.last_thata
        if dthata > 180:
            dthata = dthata - 360
        elif dthata < -180:
            dthata = dthata + 360
        self.last_thata = thata
        return dthata

    def getOdometry(self):
        '''
        Return a tuple of odometry (dxy in mm,dthata in degree, dt in s) and
        send move commands to the drone
        '''
        # Move the drone
        if in_air & (not TESTING):
            if cmd == 2:
                self.drone.move(0, -DRONE_SPEED, 0, 0)
            elif self.cmd == 3:
                self.drone.move(0, 0, 0, DRONE_SPEED)
            elif self.cmd == 4:
                self.drone.move(0, 0, 0, -DRONE_SPEED)

        # Get odometry data
        dt = self.get_dt()
        dthata = self.calc_dthata(self.drone.navdata.get(0, dict())
        .get('psi', 0))
        if self.correct_psi & (math.fabs(dthata) > 20):
            dthata = 0
            self.correct_psi = False

        dx = self.calc_distance(self.drone.navdata.get(0, dict())
        .get('vx', 0), dt)
        dy = self.calc_distance(self.drone.navdata.get(0, dict())
        .get('vy', 0), dt)
        dxy = math.sqrt(dx*dx+dy*dy)

        data = dxy, dthata, dt

        if(self.log):
            self.out.write("%f %f %f\n" % data)

        return data

    def move(self, cmd):
        '''
        Set the moving command
        '''
        self.cmd = int(cmd)

    def initialize(self):
        '''
        Let the drone fly
        '''
        print "Take off"
        if not TESTING:
            self.drone.takeoff()
            x = 0
            # Check if the drone is in air and hovering
            while self.in_air == False:
                if (self.drone.navdata.get(0, dict()).
                get('state', 0) == 4) or (x == 10):
                    self.in_air = True
                x += 1
                time.sleep(1)
            # TODO: Testing
        self.in_air = True
        print "Drone in air!"

    def shutdown(self):
        '''
        Close application
        '''
        print "Shutting down..."
        self.in_air = False
        self.drone.land()
        self.cam.release()
        self.drone.halt()
        print "Drone shutted down."
