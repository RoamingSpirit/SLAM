'''
Class for the routing.
             
author: Nils Bernhardt 
'''

from collections import deque
import math

from router import Router
from FrountierExplore.tentaclefe import TentacleFE

class TentacleRouter(Router):

    
    def __init__(self, mapconfig, ROBOT_SIZE_METERS, min_distance):
        prev_positions = deque()
        self.mapconfig = mapconfig
        self.SCAN_DIST_PIXELS = 3500 #todo
        tentacles = self.calcTentacles(mapconfig.mToPixels(ROBOT_SIZE_METERS), self.SCAN_DIST_PIXELS)
        self.fe = TentacleFE(mapconfig, tentacles, 50, 4000) #TODO

    def getRoute(self, position, mapbytes):
        '''
        Return a queue of targetpoints (x_mm, y_mm)
        '''
        return deque([(0,0),(0,0)])

    def calcTentacles(self, robot_size, dist):
        return int(2 * math.pi * dist / robot_size+1)
    
    def getNext(self, x_pixels, y_pixels, mapbytes):
        '''
        Return a targetpoint (x_pixels, y_pixels)
        '''
        frontiers = fe.findFrontiers((x_pixels, y_pixels), mapbytes, self.mapconfig.SIZE_PIXELS)
        
        
        if(len(frontiers)==0):
            if(len(self.prev_position) == 0):
                ##do deep search
                return None
            else:
                return self.prev_position.popleft()
        else:
            self.prev_positions.append((x_pixels, y_pixels))
            return frontiers.get()
       
