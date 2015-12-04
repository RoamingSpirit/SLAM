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


from sensor.xtion import XTION
from sensor.xtion import FileXTION
from sensor.Neato import NEATO
from network.server import Server
from vehicle.filedrone import FileDrone

from mapconfig import MapConfig

from vehicle.drone import Drone
from vehicle.networkvehicle import NetworkVehicle
from vehicle.commands import Commands
                
from breezyslam.algorithms import Deterministic_SLAM,RMHC_SLAM
from slam.rmhcslam import My_SLAM

from pgmutils.pgm_utils import pgm_save

from navigation.navigation import Navigation

from sys import exit, stdout
from time import time
import cv2
import sys, termios, atexit
from select import select
import math


#wait for client for image stream
stream = True
#read form log file or use sensor
readlog = True
use_odometry = True 

# Map size, scale
MAP_SIZE_PIXELS          =  1000
MAP_SIZE_METERS          =  40
seed = 9999
ROBOT_SIZE_METERS = 0.4


#for keyboard interrupt
fd = sys.stdin.fileno()
new_term = termios.tcgetattr(fd)
old_term = termios.tcgetattr(fd)

# new terminal setting unbuffered
new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)


def main(g = 0.4, h = 0.4):

   


    

    filename ='map_%f_%f' % (g,h)
    """
    if(use_odometry):
        filename += 'withodometry_'
    if(readlog):
        filename += 'fromlog_'
    if(seed==0):
        filename += 'deterministic'
    else:
        filename += ('rmhc_seed' + str(seed))
    """
    
    #initialize the asus xtion as sensor
    if(readlog):
        sensor = FileXTION("log")
    else:
        sensor = NEATO()#XTION()

    
            
    # Create a CoreSLAM object with laser params and optional robot object
    slam = My_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS, random_seed=seed, g=g, h=h) \
        if seed \
        else Deterministic_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS) 

    robot = None

    #initialiye robot
    if(use_odometry):
        navigation = Navigation(slam, MapConfig(), ROBOT_SIZE_METERS, 100, 1200, Commands)
        navigation.start()
        if(readlog):
            robot = FileDrone("odometry")
        else:
            robot = Drone()
            #robot.initialize()
    if(stream):
        server = Server(slam, MAP_SIZE_PIXELS, robot)
        server.start()

    
    # Start with an empty trajectory of positions
    trajectory = []

    # Start timing
    start_sec = time()
    
    # Loop
    atexit.register(set_normal_term)
    set_curses_term()
    
    scanno = 0

    dist = 0
    zeit = 0

    ##make initial scan
    scan = sensor.scan()
    
    while(True):
        scanno+=1
        if use_odometry:
            ##navigaiton
            # Create a byte array to receive the computed maps
            mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
    
            # Get final map    
            #slam.getmap(mapbytes)
            
            command = navigation.update(scan)

            ##odometry
            velocities = robot.move(command)
            dist += velocities[0]
            zeit += velocities[2]

            ##lidar
            scan = sensor.scan()
            
            if(len(scan)<=0):
                print 'Reader error or end of file.'
                break
            
            # Update SLAM with lidar and velocities
            slam.update(scan, velocities)


        else:
            scan = sensor.scan()
            if(len(scan)<=0):
                print 'Reader error or end of file.'
                break
        
            # Update SLAM with lidar alone
            slam.update(scan)
                    
        # Get new position
        x_mm, y_mm, theta_degrees = slam.getpos()    
        
        # Add new position to trajectory
        trajectory.append((x_mm, y_mm))


        if kbhit():
            break

    
    if(use_odometry):
        robot.shutdown()
        navigation.stop()
        
    # Report elapsed time   
    elapsed_sec = time() - start_sec
    print('\n%d scans in %f sec = %f scans / sec' % (scanno, elapsed_sec, scanno/elapsed_sec))

    print ('dist traveled:%f mm in %fs' % (dist, zeit))         
                                
    mapbytes = createMap(slam, trajectory)

           
    # Save map and trajectory as PGM file
    pgm_save(filename, mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))

    
    image = cv2.imread(filename, 0)
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


##get arguments
g = 0.1
h = 0.1

if(len(sys.argv)>1):
    if(sys.argv[1] == "help"):
        print "Run with default g = 0.1 and h = 0.1 or specify with first two arguments."
    else:
        if(len(sys.argv) != 3):
            print "Invalid amount of arguments. Zero or two."
        else:
            main(float(sys.argv[1]), float(sys.argv[2]))
else:
    main(g, h)

