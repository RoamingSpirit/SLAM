# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

import libardrone
import cv2
import time
from vehicle import Vehicle

class Drone(Vehicle):
    """
    Class representing a connection to the ARDrone, controls it and receive navdata information
    """

    def __init__(self):
        """
        Initialize the connection and variables
        """
        print "Connecting..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        cv2.namedWindow('Front camera')
        # Counter for file names
        self.frame_count=1
        self.running = True
        # 'Traveled' distance in mm
        self.distance_frame = 0.0
        self.psi_update = self.drone.navdata.get(0, dict()).get('psi', 0)
        self.timestamp_frame = 0.0
        self.timestamp_update = 0.0

    def get_information(self): 
        """
        Receive navdata information and set them on the frame
        """        
        self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0))

        # creating battery information string
        battery_str = "Battery: "
        battery_str += str(self.drone.navdata.get(0, dict()).get('battery', 0))
        battery_str += "%"
        cv2.putText(self.frame, battery_str, (10,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        
    def save_frame(self):
        """
        Save current frame
        """
        file = "Frames/#"
        file += str(self.frame_count)
        file += ".jpg"
        cv2.imwrite(file,self.frame)
        self.frame_count += 1
        print "Frame saved"
        
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
        if vx < 0.0:
            vx = 0.0
        self.distance_frame += (vx*self.get_dt_frame())
        if self.distance_frame < 0.0:
            self.distance_frame = 0.0
        else:
            self.distance_frame=round(self.distance_frame, 0)
            
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
        return self.update(self.drone.navdata.get(0, dict()).get('psi', 0))    
        
    def run(self):
        """
        Main loop
        """
        while self.running:
            # get current frame of video
            self.running, self.frame = self.cam.read()
            self.get_information()
            if self.running:     
                # show current frame
                cv2.imshow('Front camera', self.frame)
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
                elif k==112:  # p
                    self.save_frame()
                elif k==117:  # u
                    print self.getOdometry()
                elif k==-1:  # other
                    continue
                else:
                    print k
            else:
                # error reading frame
                print "Error reading video feed"
                
    def shutdown(self):
        """
        Close application
        """
        print "Shutting down..."
        self.cam.release()
        cv2.destroyAllWindows()
        self.drone.halt()
        print "Ok."
