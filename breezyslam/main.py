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
import sys


#seed for RMHC
SEED = 9999
#LIDAR offset from the center which must be checked for obstacles
RELEVANT_LIDARS = 80
#Distance the robot should keep from any obstacle in mm
SECURITY_DIST_MM = 800

def main(log, readlog, only_odometry, sensorFile, odomFile, resultname, mapconfig):
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
            if(command == None):
                print "Navigation terminated."
                break

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
                break

            #Update SLAM
            slam.update(scan, velocities)

            # Get new position
            x_mm, y_mm, theta_degrees = slam.getpos()    
        
            # Add new position to trajectory
            trajectory.append((x_mm, y_mm))

    except KeyboardInterrupt:
        print "Program stoped!"
    finally:
        print "Shutting down."
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
        mapconfig.safeaspng(mapbytes, resultname)


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


#________________________________READ_ARGUMENTS______________________________________#

log = False
readlog = False
only_odometry = False
sensorFile = "log"
odomFile = "odometry"
resultname = "result"
size_pixels = 1000
size_meters = 40
helptext = ("Specify parameters (e.g log=true to perform logging). \n" +
            "log: true if data should be stored. Default false. \n" +
            "readlog: true if data should be read from logfile. Default false. \n" +
            "deterministic: true if just odometry, no rmhc should be used. Default false. \n" +
            "sensor: file from which the sensor data should be read. Default log. \n" +
            "odometry: file from which the odometry data should be read. Default odometry. \n" +
            "result: filename for the created map. Default result. \n" +
            "pixels: size of the map in pixels. Default 1000. \n" +
            "meters: size of the map in meters. Default 40. \n")

if(len(sys.argv)>1):
    if(sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "-help"):
        #print help
        print helptext
        sys.exit()
    else:
        for arg in sys.argv:
            values = arg.split('=')
            if(len(values)==2):
                if(values[0] == "log"):
                    if(values[1] == "true"): log = True
                    elif(values[1] == "false"): log = False
                    else:
                        print "Unknown argument value for log. true or false"
                        print helptext
                        sys.exit()
                        
                elif(values[0] == "readlog"):
                    if(values[1] == "true"): readlog = True
                    elif(values[1] == "false"): readlog = False
                    else:
                        print "Unknown argument value for readlog. true or false"
                        print helptext
                        sys.exit()
                        
                elif(values[0] == "deterministic"):
                    if(values[1] == "true"): only_odometry = True
                    elif(values[1] == "false"): only_odometry = False
                    else:
                        print "Unknown argument value for deterministic. true or false"
                        print helptext
                        sys.exit()

                elif(values[0] == "sensor"):
                    if(len(values[1]) > 0): sensorFile = values[1]
                    else:
                        print "Bad filename for sensor."
                        print helptext
                        sys.exit()
                
                elif(values[0] == "odometry"):
                    if(len(values[1]) > 0): odomFile = values[1]
                    else:
                        print "Bad filename for odometry."
                        print helptext
                        sys.exit()

                elif(values[0] == "result"):
                    if(len(values[1]) > 0): resultname = values[1]
                    else:
                        print "Bad filename for result."
                        print helptext
                        sys.exit()
                        
                elif(values[0] == "pixels"):
                    try:
                        size_pixels = int(values[1])
                    except ValueError:
                        print "Bad value for pixels."
                        print helptext
                        sys.exit()

                elif(values[0] == "meters"):
                    try:
                        size_meters = int(values[1])
                    except ValueError:
                        print "Bad value for meters."
                        print helptext
                        sys.exit()

                else:
                    print "Unknown parameter: " + value[0]
                    print helptext
                    sys.exit()
            
mapconfig = MapConfig(size_pixels, size_meters)

main(log, readlog, only_odometry, sensorFile, odomFile, resultname, mapconfig)



        
