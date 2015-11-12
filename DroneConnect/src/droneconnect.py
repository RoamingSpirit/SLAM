# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

import libardrone
import cv2
import time

class DroneConnect:
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
        self.distance_update = 0.0
        self.psi_frame = self.drone.navdata.get(0, dict()).get('psi', 0)
        self.psi_update = self.drone.navdata.get(0, dict()).get('psi', 0)
        self.old_timestamp = 0.0
        self.new_timestamp = 0.0

    def get_information(self): 
        """
        Receive navdata information and set them on the frame
        """        
        self.calc_distance(self.drone.navdata.get(0, dict()).get('vx', 0), self.get_dt())
        
        # create distance string
        distance_str = "distance: "
        distance_str += str(self.distance_update)
        cv2.putText(self.frame, distance_str, (10,320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        
        # create psi string
        psi_str = "psi: "
        psi_str += str(self.psi_update)
        cv2.putText(self.frame, psi_str, (10,335), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        
        """
         # creating altitude information string
        altitude_str = "altitude: "
        altitude_str += str(self.drone.navdata.get(0, dict()).get('altitude', 0))
        cv2.putText(self.frame, altitude_str, (10,275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating theta information string
        theta_str = "theta: "
        theta_str += str(self.drone.navdata.get(0, dict()).get('theta', 0))
        cv2.putText(self.frame, theta_str, (10,290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating phi information string
        phi_str = "phi: "
        phi_str += str(self.drone.navdata.get(0, dict()).get('phi', 0))
        cv2.putText(self.frame, phi_str, (10,305), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating vx information string
        vx_str = "vx: "
        vx_str += str(round(self.drone.navdata.get(0, dict()).get('vx', 0)))
        cv2.putText(self.frame, vx_str, (10,320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating vy information string
        vy_str = "vy: "
        vy_str += str(round(self.drone.navdata.get(0, dict()).get('vy', 0)))
        cv2.putText(self.frame, vy_str, (10,335), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        """

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
        self.distance_update = self.distance_frame
        self.distance_frame = 0.0
        # psi
        self.psi_update = psi - self.psi_frame
        self.psi_frame = psi
        
    def get_dt(self):
        if self.old_timestamp == 0.0:
            self.old_timestamp = time.time()
            return 0.0
        self.new_timestamp = time.time()
        dt = self.new_timestamp-self.old_timestamp
        self.old_timetamp = self.new_timestamp
        return dt
        
    def calc_distance(self, vx, dt):
        """
        Calculate distance since last frame
        """
        if vx < 0.0:
            vx = 0.0
        self.distance_frame += (vx*dt)/1000
        if self.distance_frame < 0.0:
            self.distance_frame = 0.0
        else:
            self.distance_frame=round(self.distance_frame, 0)
            
    def calc_psi(self, psi):
        """
        Calculate psi since last frame
        """
        self.psi_frame += psi - self.psi_frame
        
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
                    self.update(self.drone.navdata.get(0, dict()).get('psi', 0))
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
