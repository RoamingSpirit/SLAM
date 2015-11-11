'''
log2pgm.py : BreezySLAM Python demo.  Makes scans with an ASUS xtion and produces a .PGM image file showing robot 
             trajectory and final map.
             
For details see

    @inproceedings{coreslam-2010,
      author    = {Bruno Steux and Oussama El Hamzaoui}, modified by Nils Bernhardt
      title     = {CoreSLAM: a SLAM Algorithm in less than 200 lines of C code},
      booktitle = {11th International Conference on Control, Automation, 
                   Robotics and Vision, ICARCV 2010, Singapore, 7-10 
                   December 2010, Proceedings},
      pages     = {1975-1979},
      publisher = {IEEE},
      year      = {2010}
    }
                 
Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.

Change log:

20-APR-2014 - Simon D. Levy - Get params from command line
05-JUN-2014 - SDL - get random seed from command line
'''


from sensor import XTION
from server import Server

from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM

from pgm_utils import pgm_save

from sys import exit, stdout
from time import time
import cv2
import sys, termios, atexit
from select import select


#wait for client for image stream
stream = True

# Map size, scale
MAP_SIZE_PIXELS          =  1000
MAP_SIZE_METERS          =  30
seed = 9999 #whit is this used for?
use_odometry = False #not yet implemented
iterations = 600 #how many scans to make


#for keyboard interrupt
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)


def main():
   
    #initialize the asus xtion as sensor
    sensor = XTION()

    #initialiye robot
    if(use_odometry):
        robot = 0#todo initialize a vehicle
            
    # Create a CoreSLAM object with laser params and optional robot object
    slam = RMHC_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS, 100, 300, random_seed=seed) \
        if seed \
        else Deterministic_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS) 

    if(stream):
        server = Server(slam, MAP_SIZE_PIXELS)
        server.start()
    
    # Start with an empty trajectory of positions
    trajectory = []

    # Start timing
    start_sec = time()
    
    # Loop
    atexit.register(set_normal_term)
    set_curses_term()
    
    scanno = 0
    
    
    while(True):
        scanno+=1
        if use_odometry:
            velocities = robot.getOdometry()
            scan = sensor.scan()
                                 
            # Update SLAM with lidar and velocities
            slam.update(sensor.scan(), velocities)
            
        else:
        
            # Update SLAM with lidar alone
            slam.update(sensor.scan())
                    
        # Get new position
        x_mm, y_mm, theta_degrees = slam.getpos()    
        
        # Add new position to trajectory
        trajectory.append((x_mm, y_mm))

        if kbhit():
            break

    # Report elapsed time
    elapsed_sec = time() - start_sec
    print('\n%d scans in %f sec = %f scans / sec' % (scanno, elapsed_sec, scanno/elapsed_sec))
                    
                                
    mapbytes = createMap(slam, trajectory)

           
    # Save map and trajectory as PGM file    
    pgm_save('test.pgm', mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
    image = cv2.imread("test.pgm", 0)
    print"Accessing the image.. again. So dirty."
    print"Saving as .png: ..."
    cv2.imwrite("test.png", image)
    if(stream):
        server.close()
    print "done"

# Helpers ---------------------------------------------------------        

def createMap(slam, trajectory):
    # Create a byte array to receive the computed maps
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
    
    # Get final map    
    slam.getmap(mapbytes)
    
    # Put trajectory into map as black pixels
    for coords in trajectory:
                
        x_mm, y_mm = coords
                               
        x_pix = mm2pix(x_mm)
        y_pix = mm2pix(y_mm)
                                                                                              
        mapbytes[y_pix * MAP_SIZE_PIXELS + x_pix] = 0;
        
    return mapbytes

# switch to normal terminal
def set_normal_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

# switch to unbuffered terminal
def set_curses_term():
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []

def mm2pix(mm):
        
    return int(mm / (MAP_SIZE_METERS * 1000. / MAP_SIZE_PIXELS))  


main()
