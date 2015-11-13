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
    first = True
    # 'Traveled' distance in mm
    distance_frame = 0.0
    timestamp_frame = 0.0
    timestamp_update = 0.0

    def __init__(self):
        """
        Initialize the connection and variables
        """
        threading.Thread.__init__(self)
        print "Connecting..."
        #self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        self.psi_update = self.drone.navdata.get(0, dict()).get('psi', 0)
        #cv2.namedWindow('Front camera')
        # Counter for file names
        self.start()
        
    def update(self, psi):
        # distance
        dx = self.distance_frame
        self.distance_frame = 0.0
        return dx,self.calc_psi(psi),self.get_dt_update()
        
    def calc_dt(self,old):
        """
        Return the time difference between old time and now
        """
        now = time.time()
        if old == 0.0:
            return 0.0,now
        dt = now-old
        return dt, now
    
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
        
    def calc_distance(self, vx):
        """
        Calculate distance since last frame
        """
        self.distance_frame += (vx*self.get_dt_frame())
        self.distance_frame=round(self.distance_frame, 2)
        #print vx,self.distance_frame
            
    def calc_psi(self, psi):
        """
        Calculate psi since last call
        """
        dd = psi - self.psi_update
        self.psi_update = psi
        return dd
        
    def getOdometry(self):
        """
        return a tuple of odometry (dxy in mm,dthata in degree, dt in s)
        """
        if self.first:
            self.first = False
            return 0.0,0,0.0
        return self.update(self.drone.navdata.get(0, dict()).get('psi', 0))
        
    def shutdown(self):
        """
        Close application
        """
        print "Shutting down..."
        #self.cam.release()
        #cv2.destroyAllWindows()
        self.running = False
        self.drone.halt()
        print "Drone shutted down."
        
    def takeoff(self):
        """
        Lets the drone fly
        """
        print "Take off"
        #drone.takeoff()
    
    def run(self):
        """
        Main loop
        """
        while self.running:
            # get current frame of video
            #self.running, self.frame = self.cam.read()
            self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0))
            print self.getOdometry()
            time.sleep(0.05)
            # show current frame
            #cv2.imshow('Front camera', self.frame)
            """
            k = cv2.waitKey(1)
            if k==27:   # Esc
                self.running = False
                self.shutdown()
            elif k==10:  # Return
                self.drone.takeoff()
                print "Return pressed"
            elif k==32:  # Space
                self.drone.land()
                print "Space pressed"
            elif k==119:  # w
                self.drone.move_forward()
                print "W pressed"
            elif k==97:  # a
                self.drone.move_left()
                print "A pressed"
            elif k==115:  # s
                self.drone.move_backward()
                print "S pressed"
            elif k==100:  # d
                self.drone.move_right()
                print "D pressed"
            elif k==65362:  # Up
                self.drone.move_up()
                print "Up pressed"
            elif k==65364:  # Down
                self.drone.move_down()
                print "Down pressed"
            elif k==65361:  # Left
                self.drone.turn_left()
                print "Left pressed"
            elif k==65363:  # Right
                self.drone.turn_right()
                print "Right pressed"
            elif k==117:  # u
                print self.getOdometry()
            elif k==-1:  # other
                continue
            else:
                print k"""
