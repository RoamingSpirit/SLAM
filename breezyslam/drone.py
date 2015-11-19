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
from vehicle import Vehicle

class Drone(Vehicle):
    """
    Class representing a connection to the ARDrone,
    controls it and receive navdata information
    """
    DRONE_SPEED = 0.2
    correct_psi = True
    in_air = False
    moving = False
    turning = False
    cmd = [0,0,0]
    old_timestamp = 0.0

    def __init__(self, log = True):
        """
        Initialize the connection and variables
        """
        self.log = log
        if(log):
            self.out = open('odometry', 'w')
        print "Connecting..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        self.last_thata = self.drone.navdata.get(0, dict()).get('psi', 0)

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
        dx = vx*dt
        if self.moving:
            self.distance -= dx
        return dx

    def calc_dthata(self, thata):
        """
        Calculate dthata since last call
        """
        dthata = thata - self.last_thata
        if dthata > 180:
            dthata = dthata - 360
        elif dthata < -180:
            dthata = dthata + 360
        self.last_thata = thata
        
        if self.turning:
            self.angle -= dthata
        return dthata

    def getOdometry(self):
        """
        Return a tuple of odometry (dxy in mm,dthata in degree, dt in s) and
        send move commands to the drone
        """
        # Move the drone
        if self.moving or self.turning:
            if cmd[0] == 0:
                self.drone.move(0, -self.DRONE_SPEED, 0, self.DRONE_SPEED)
            elif cmd[0] == 1:
                self.drone.move(0, -self.DRONE_SPEED, 0, -self.DRONE_SPEED)
        else:
            self.drone.hover()

        # Get odometry data
        dt = self.get_dt()
        dthata = self.calc_dthata(self.drone.navdata.get(0, dict()).get('psi', 0))
        if self.correct_psi & (math.fabs(dthata) > 20):
                dthata = 0
                self.correct_psi = False
        data = self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0), dt), dthata, dt
        self.update_commands()
                
        if(self.log):
                self.out.write("%f %f %f\n" % data)

        return data
    
    def update_commands(self):
        """
        Update the command list
        """
        # Move command
        if self.cmd[2] < 0 & self.moving:
            self.cmd[2] = 0
            self.moving = False

        # Turn command
        if self.cmd[0] == 0:
            if self.cmd[1] < 0:
                self.cmd[1] = 0
                self.turning = False
        elif self.cmd[0] == 1:
            if self.cmd[1] > 0:
                self.cmd[1] = 0
                self.turning = False

    def move(self, dxy):
        """
        Set the distance to move forward
        """
        if dxy < 0:
            self.cmd[2] = 0
        else:
            self.cmd[2] = dxy
            self.moving = True

    def turn(self, dtheta):
        """
        Set the turn angle
        """
        if dtheta < 0:
            self.cmd[0] = 1
        elif dtheta > 0:
            self.cmd[0] = 0
        self.cmd[1] = dtheta
        self.turning = True

    def initialize(self):
        """
        Let the drone fly
        """
        print "Take off"
        self.drone.takeoff()
        print "Drone in air!"

    def shutdown(self):
        """
        Close application
        """
        print "Shutting down..."
        self.drone.land()
        self.moving = False
        self.turning = False
        self.cam.release()
        self.drone.halt()
        print "Drone shutted down."