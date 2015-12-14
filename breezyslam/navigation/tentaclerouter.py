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
        if(target == None): return None
        x_mm = self.mapconfig.pixelsTomm(target[0])
        y_mm = self.mapconfig.pixelsTomm(target[1])
        return deque([(x_mm, y_mm)])

    def calcTentacles(self, robot_size, dist):
        return int(2 * math.pi * dist / robot_size * 2)
    
    def getNext(self, x_pixels, y_pixels, mapbytes):
        '''
        Return a targetpoint (x_pixels, y_pixels)
        '''
        frontiers = self.fe.findFrontiers((x_pixels, y_pixels), mapbytes, self.mapconfig.SIZE_PIXELS)


        """
        add for displaying frontiers in the map
        best = frontiers.get()

        while(not frontiers.empty()):
            pos = frontiers.get()
            self.mapconfig.drawCross(pos[1][0], pos[1][1], 20, 255, mapbytes)
        return best[1]
        """
        
        if(frontiers.empty()):
            return None
        else:
            return frontiers.get()[1]
       
