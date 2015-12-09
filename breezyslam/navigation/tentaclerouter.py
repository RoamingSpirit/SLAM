'''
Class for the routing.
             
author: Nils Bernhardt 
'''

from collections import deque
import math

from router import Router
from FrontierExplorer.tentaclefe import TentacleFE

class TentacleRouter(Router):

    
    def __init__(self, mapconfig, ROBOT_SIZE_METERS, min_distance):
        self.prev_positions = []
        self.mapconfig = mapconfig
        self.SCAN_DIST_PIXELS = mapconfig.mmToPixels(3500) #todo
        tentacles = self.calcTentacles(mapconfig.mToPixels(ROBOT_SIZE_METERS), self.SCAN_DIST_PIXELS)
        self.fe = TentacleFE(mapconfig, tentacles, mapconfig.mmToPixels(500), mapconfig.mmToPixels(5000)) #TODO

    def getRoute(self, position, mapbytes):
        '''
        Return a queue of targetpoints (x_mm, y_mm)
        '''
        x_pixels = self.mapconfig.mmToPixels(position[0])
        y_pixels = self.mapconfig.mmToPixels(position[1])

        target = self.getNext(x_pixels, y_pixels, mapbytes)
        x_mm = self.mapconfig.pixelsTomm(target[0])
        y_mm = self.mapconfig.pixelsTomm(target[1])
        return deque([(x_mm, y_mm)])

    def calcTentacles(self, robot_size, dist):
        print dist, robot_size
        return int(2 * math.pi * dist / robot_size * 2)
    
    def getNext(self, x_pixels, y_pixels, mapbytes):
        '''
        Return a targetpoint (x_pixels, y_pixels)
        '''
        frontiers = self.fe.findFrontiers((x_pixels, y_pixels), mapbytes, self.mapconfig.SIZE_PIXELS)

        
        if(frontiers.empty()):
            if(len(self.prev_positions) == 0):
                ##do deep search
                print "No frontiers found. No previous possition."
                return None
            else:
                print "No frontiers foud. Going to previous position"
                return self.prev_positions.pop()
        else:
            print "Returning first frontier"
            self.prev_positions.append((x_pixels, y_pixels))
            return frontiers.get()[1]
       
