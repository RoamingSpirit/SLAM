'''
Class for the navigation.
             
author: Nils Bernhardt 
'''

import threading
import time

MOVE_FORWARD = 2
TURN_RIGHT = 3
TURN_LEFT = 4
STAGNATE = 5

class Navigation(threading.Thread):

    

    def __init__(self, slam, MAP_SIZE_PIXELS, MAP_SIZE_METERS, ROBOT_SIZE_METERS, offset_in_scan, min_distance):
        """
        MAP_SIXE_PIXELS: map size in pixel
        MAP_SIZE_METERS: map size in meters
        ROBOT_SZIE_METERS: robot size in meters
        offset_in_scan: values to check in a scan for obstacles from the center
        min_distance: minimum distance to keep to obstacles
        """
        threading.Thread.__init__(self)
        self.slam = slam
        self.MAP_SIZE_PIXELS = MAP_SIZE_PIXELS
        self.MAP_SIZE_METERS = MAP_SIZE_METERS
        self.ROBOT_SIZE_METERS = ROBOT_SIZE_METERS
        self.mapbytes = self.createMap()
        self.command = MOVE_FORWARD
        self.recalculate = True
        self.offset_in_scan = offset_in_scan
        self.min_distance = min_distance
    
    def run(self):
        '''
        Do the navigation calculation here.
        '''
        self.running = True
        while(self.running):
            ##TODO Mapping navigation
            time.sleep(5)
            self.mapbytes = self.createMap()
            self.position = self.slam.getpos()
            print self.position
        

    def update(self, scan):
        """
        return a move command based on the navigation and the scan
        """
        ##TODO Update command
        if(self.command == MOVE_FORWARD):
            print self.offset_in_scan, self.min_distance
            ##Check scan for obstacles in front
            if(self.checkTrajectory(scan, self.offset_in_scan, self.min_distance)== False):
                ##recalcualte route
                self.recalcualte = True
                print "obstacle detected"
                return STAGNATE
             
        ##turn and stay should be always possible
        return self.command

    def checkTrajectory(self, scan, offset, min_distance):
        """
        Checks if the Trajectory in front is free.
        scan: current scan with center on the trajectory
        offset: values to check in scan for obstacles
        min_distance: minimum distance to obstacles in the trajectory
        return: True if Trajecotry is free
        """
        center = len(scan)/2
        for i in range(center-offset, center+offset):
            if(scan[i] < min_distance & scan[i] > 0):
                return False
        return True

    def createMap(self):
        """
        creates the map and stores it a byte array.
        """
        # Create a byte array to receive the computed maps
        mapbytes = bytearray(self.MAP_SIZE_PIXELS * self.MAP_SIZE_PIXELS)
    
        # Get final map    
        self.slam.getmap(mapbytes)

        return mapbytes

    def stop(self):
        """
        Stops navigation.
        """
        self.running = False

    def getmapbytes(self):
        """
        Returns the last received mapbytes
        """
        if(self.mapbytes == None):
            self.mapbytes = self.createMap()
        return self.mapbytes
        

    
