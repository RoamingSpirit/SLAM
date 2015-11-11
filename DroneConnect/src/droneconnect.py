# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

import libardrone
import cv2

class DroneConnect:

    def __init__(self):
        print "Connecting..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Ok."
        self.frame_count=1
        self.running = True
        cv2.namedWindow('Front camera')

    def get_information(self):
         # creating altitude information string
        altitude = "altitude: "
        altitude += str(self.drone.navdata.get(0, dict()).get('altitude', 0))
        cv2.putText(self.frame,altitude, (10,260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        
        #print self.drone.navdata

        # creating theta information string
        theta = "theta: "
        theta += str(self.drone.navdata.get(0, dict()).get('theta', 0))
        cv2.putText(self.frame,theta, (10,275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating phi information string
        phi = "phi: "
        phi += str(self.drone.navdata.get(0, dict()).get('phi', 0))
        cv2.putText(self.frame,phi, (10,290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating vx information string
        vx = "vx: "
        vx += str(round(self.drone.navdata.get(0, dict()).get('vx', 0)))
        cv2.putText(self.frame,vx, (10,305), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating vy information string
        vy = "vy: "
        vy += str(round(self.drone.navdata.get(0, dict()).get('vy', 0)))
        cv2.putText(self.frame,vy, (10,320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating vz information string
        vz = "vz: "
        vz += str(round(self.drone.navdata.get(0, dict()).get('vz', 0)))
        cv2.putText(self.frame,vz, (10,335), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        # creating battery information string
        battery = "Battery: "
        battery += str(self.drone.navdata.get(0, dict()).get('battery', 0))
        battery += "%"
        cv2.putText(self.frame,battery, (10,350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
        
    def save_frame(self):
        file = "Frames/#"
        file += str(self.frame_count)
        file += ".jpg"
        cv2.imwrite(file,self.frame)
        self.frame_count += 1
        print "Frame saved"
        
    def run(self):
        while self.running:
            # get current frame of video
            self.running, self.frame = self.cam.read()
            self.get_information()
            if self.running:     
                # show current frame
                cv2.imshow('Front camera', self.frame)
                k = cv2.waitKey(1)
                if k==27:   # esc key to stop
                    self.running = False
                    self.shutdown()
                elif k==10:  # return
                    self.drone.takeoff()
                    print "Return pressed"
                elif k==32:  # space
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
                elif k==65362:  # up
                    self.drone.move_up()
                    print "Up pressed"
                elif k==65364:  # down
                    self.drone.move_down()
                    print "Down pressed"
                elif k==65361:  # left
                    self.drone.turn_left()
                    print "Left pressed"
                elif k==65363:  # right
                    self.drone.turn_right()
                    print "Right pressed"
                elif k==112:  # p
                    self.save_frame()
                    print "P pressed"
                elif k==-1:  # other
                    continue
                else:
                    print k
            else:
                # error reading frame
                print 'error reading video feed'
                
    def shutdown(self):
        print "Shutting down..."
        self.cam.release()
        cv2.destroyAllWindows()
        self.drone.halt()
        print "Ok."
