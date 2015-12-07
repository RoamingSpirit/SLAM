__author__ = 'troyhughes'




from collections import deque
import math

from router import Router
from FrontierExplorer.hallwayExplorer import HallwayExplorer

class HallwayRouter(Router):


    def __init__(self, mapconfig, ROBOT_SIZE_METERS, min_distance):
        self.mapconfig = mapconfig
        self.SCAN_DIST_PIXELS = 3500
        self.fe = HallwayExplorer(mapconfig,2) #TODO

    def getRoute(self, position, mapbytes):
        '''
        Return a queue of targetpoints (x_mm, y_mm)
        '''
        x_pixels = self.mapconfig.mmToPixels(position[0])
        y_pixels = self.mapconfig.mmToPixels(position[1])
        return deque([self.getNext(x_pixels, y_pixels, mapbytes)])


    def getNext(self, x_pixels, y_pixels, mapbytes):
        """
        This gets the next frontier to explore.

        :param x_pixels: x pixle of the robot
        :param y_pixels: y pixle of the robot
        :param mapbytes: 2d representation of the map
        :return: (x,y) touple of the goal
        """
        '''
        Return a targetpoint (x_pixels, y_pixels)
        '''
        frontiers = self.fe.findFrontiers((x_pixels, y_pixels), mapbytes, self.mapconfig.SIZE_PIXELS)


        if(frontiers.empty()):
            raise NotImplementedError("Hallway Explorer has run out of frontiers to explore")
        else:
            return frontiers.get()[1]

