'''
Class for the navigation.
             
author: Nils Bernhardt 
'''

from router import Router
from tentaclerouter import TentacleRouter

import threading
import time
import math

ANGLE_TOLERANCE_DEGREE = 5 #tolerance for moving forward
TARGET_TOLERANCE_MM = 500 #min dist to target

class Navigation(threading.Thread):

    route_lock = threading.Condition()
    route = None
    target = None
    
    def __init__(self, slam, mapconfig, ROBOT_SIZE_METERS, offset_in_scan, min_distance, commands):
        """
        MAP_SIXE_PIXELS: map size in pixel
        MAP_SIZE_METERS: map size in meters
        ROBOT_SZIE_METERS: robot size in meters
        offset_in_scan: values to check in a scan for obstacles from the center
        min_distance: minimum distance to keep to obstacles
        commans: costants for commands
        """
        self.commands = commands
        threading.Thread.__init__(self)
        self.slam = slam
        self.mapconfig = mapconfig
        self.ROBOT_SIZE_METERS = ROBOT_SIZE_METERS
        self.mapbytes = self.createMap()
        self.recalculate = True
        self.offset_in_scan = offset_in_scan
        self.min_distance = min_distance
        self.router = TentacleRouter(mapconfig, ROBOT_SIZE_METERS, min_distance)
    
    def run(self):
        '''
        Recalcualtes a new route if necessary
        '''
        self.running = True
        while(self.running):
            
            if(self.recalculate):                
                self.mapbytes = self.createMap()
                self.position = self.slam.getpos()
                print self.position
                route = self.router.getRoute(self.position, self.mapbytes)
                self.recalculate = False
                
                self.route_lock.acquire()
                self.route = route
                self.route_lock.release()
            else:
                self.route_lock.acquire()
                self.route_lock.wait()
                self.route_lock.release()
        print "Navigation terminated"            
            
        

    def update(self, scan):
        """
        return a move command based on the navigation and the scan
        """
        command = self.getCommand()
        if(command == self.commands.MOVE_FORWARD):
            #check scan for obstacles in front
            if(self.checkTrajectory(scan, self.offset_in_scan, self.min_distance)== False):
                #recalcualte route
                self.recalculate = True
                
                self.route_lock.acquire()
                self.route_lock.notify()
                self.route_lock.release()
                
                return self.commands.WAIT
             
        #turn and stay should be always possible
        return command

    def getCommand(self):
        """
        returns the next movement to perform
        """
        #check if currently recalculating ==> wait
        if(self.recalculate): return self.commands.WAIT
        #check if no route is available ==> turn around to expand map
        if(self.route == None): return self.commands.TURN_RIGHT

        position = self.slam.getpos()

        #check if target is reached and if new targets are available
        while(self.reachedTarget(self.target, position)):
            if(len(self.route)==0):
                #recalcualte route
                self.recalculate = True
                
                self.route_lock.acquire()
                self.route_lock.notify()
                self.route_lock.release()
                return self.commands.WAIT
            else:
                self.target = self.route.popleft()

        #chek if it is not necessary to turn
        angle = self.getAngle(self.target, self.target)        
        if(math.fabs(angle) < ANGLE_TOLERANCE_DEGREE):
            return self.commands.MOVE_FORWARD

        #turn
        if(angle > 0):
            return self.commands.TURN_RIGHT
        else:
            return self.commands.TURN_LEFT

    def reachedTarget(self, target, position):
        """
        Checks if the position is in the target range
        """
        if(target == None): return True
        xd = target[0]-position[0]
        yd = target[1]-position[1]
        dist = math.sqrt(xd*xd+yd*yd)
        return dist < TARGET_TOLERANCE_MM

    def getAngle(self, target, position):
        """
        Calcualtes the angel of the line between the position and the target
        target: target position
        position: robot position
        return: anngle of the trajectory
        """
        x = float(target[0] -  position[0])
        y = float(target[1] - position[1])

        if(x == 0 and y == 0):
            return 0
        
        angle = math.degrees(math.acos(x/math.sqrt(x*x+y*y)))
        if(y<0):return -angle
                
        return angle

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
            if(scan[i] < min_distance and scan[i] > 0):
                return False
        return True

    def createMap(self):
        """
        creates the map and stores it a byte array.
        """
        # Create a byte array to receive the computed maps
        mapbytes = bytearray(self.mapconfig.SIZE_PIXELS * self.mapconfig.SIZE_PIXELS)
    
        # Get final map    
        self.slam.getmap(mapbytes)

        return mapbytes

    def stop(self):
        """
        Stops navigation.
        """
        self.running = False
        self.recalculate = False
        self.route_lock.acquire()
        self.route_lock.notify()
        self.route_lock.release()

    def getmapbytes(self):
        """
        Returns the last received mapbytes
        """
        if(self.mapbytes == None):
            self.mapbytes = self.createMap()
        return self.mapbytes
        

    
