'''
Class for the routing.
             
author: Nils Bernhardt 
'''

from collections import deque
import math

from position import Position

class TentacleRouter():

    
    def __init__(self, MAP_SIZE_PIXELS, ROBOT_SIZE_PIXELS, SCAN_DIST_PIXELS):
        prev_positions = deque()
        self.MAP_SIZE_PIXELS = MAP_SIZE_PIXELS
        self.SCAN_DIST_PIXELS = SCAN_DIST_PIXELS
        self.tentacles = self.calcTentacles(ROBOT_SIZE_PIXELS, SCAN_DIST_PIXELS)

    def calcTentacles(self, robot_size, dist):
        return int(2 * math.pi * dist / robot_size+1)
    
    def getNext(self, x_pixels, y_pixels, mapbytes):
        '''
        Return a targetpoint (x_pixels, y_pixels)
        '''
        position = Position(x_pixels, y_pixels, mapbytes, self.MAP_SZIE_PIXELS, self.tentacles, self.SCAN_DIST_PIXELS)
        target = position.getNextTarget()
        if(target == None):
            if(len(self.prev_position) == 0):
                ##do deep search
                return None
            else:
                return self.prev_position.popleft().getPosition()
        else:
            self.prev_positions.append(position)
            return target
       
