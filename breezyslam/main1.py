from sensor.xtion import XTION
from sensor.xtion import FileXTION

from network.server import Server

from vehicle.filedrone import FileDrone
from vehicle.networkvehicle import NetworkVehicle
from vehicle.commands import Commands

from mapconfig import MapConfig

from navigation.navigation import Navigation

from slam.rmhcslam import My_SLAM

from pgmutils.pgm_utils import pgm_save

from breezyslam.algorithms import Deterministic_SLAM

from time import time
import math


#seed for RMHC
SEED = 9999
#LIDAR offset from the center which must be checked for obstacles
RELEVANT_LIDARS = 50 
#Distance the robot should keep from any obstacle in mm
SECURITY_DIST_MM = 800

def main(log = False, readlog = False, only_odometry = False, sensorFile = "log", odomFile = "odometry", resultname = "result", mapconfig = MapConfig()):
    initialized = False
    sensor = None
    navigation = None
    robot = None
    server = None
    try:
        #Initialize Sensor
        if(readlog):
            sensor = FileXTION(sensorFile)
        else:
            sensor = XTION(log)

        #Initialize Slam
        if(only_odometry):
            slam = Deterministic_SLAM(sensor, mapconfig.SIZE_PIXELS, mapconfig.SIZE_METERS)
        else:
            slam = My_SLAM(sensor, mapconfig.SIZE_PIXELS, mapconfig.SIZE_METERS, random_seed = SEED)

        #Initialize Robot
        if(readlog):
            robot = FileDrone(odomFile)
        else:
            robot = NetworkVehicle()
            robot.initialize()

        #Open Controll and Map Server
        server = Server(slam, mapconfig.SIZE_PIXELS, robot)
        server.start()

        #Initialize Navigation
        navigation = Navigation(slam, mapconfig, robot.getSize(), RELEVANT_LIDARS, SECURITY_DIST_MM, Commands)
        navigation.start()

        #Monitors
        scanno = 0
        dist = 0
        timePast = 0
        trajectory = []
        start_sec = time()

        #Make initial scan
        scan = sensor.scan()

        initialized = True

        #Main loop
        while(True):
            scanno += 1

            #get command
            command = navigation.update(scan)

            #send command and get odometry
            velocities = robot.move(command)

            #check if velocities are valid
            if(velocities == None):
                print "Robot terminated."
                break

            #update monitors
            dist += velocities[0]
            timePast += velocities[2]

            #get scan
            scan = sensor.scan()

            #check if scan is valid
            if(len(scan)<=0):
                print "Sensor terminated."

            #Update SLAM
            slam.update(scan)

            # Get new position
            x_mm, y_mm, theta_degrees = slam.getpos()    
        
            # Add new position to trajectory
            trajectory.append((x_mm, y_mm))

    except KeyboardInterrupt:
        print "Program stoped!"
    finally:
        if(sensor != None): sensor.shutdown()
        if(navigation != None): navigation.stop()
        if(robot != None): robot.shutdown()
        if(server != None): server.close()

    if(initialized):
        #Print results
        elapsed_sec = time() - start_sec
        print('\n%d scans in %f sec = %f scans / sec' % (scanno, elapsed_sec, scanno/elapsed_sec))
        print ('Distance traveled:%f mm in %fs' % (dist, timePast))

        #generate map
        mapbytes = createMap(slam, trajectory, mapconfig)
        # Save map and trajectory as PGM file
        pgm_save(resultname, mapbytes, (mapconfig.SIZE_PIXELS, mapconfig.SIZE_PIXELS))


# Helpers ---------------------------------------------------------        

def createMap(slam, trajectory, mapconfig):
    # Create a byte array to receive the computed maps
    mapbytes = bytearray(mapconfig.SIZE_PIXELS * mapconfig.SIZE_PIXELS)
    
    # Get final map    
    slam.getmap(mapbytes)
    
    # Put trajectory into map as black pixels
    for coords in trajectory:
                
        x_mm, y_mm = coords
                               
        x_pix = int(mapconfig.mmToPixels(x_mm))
        y_pix = int(mapconfig.mmToPixels(y_mm))
                                                                                              
        mapbytes[y_pix * mapconfig.SIZE_PIXELS + x_pix] = 0;
        
    return mapbytes

main(readlog = True)





        
