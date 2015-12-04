'''

             
author: Nils Bernhardt 
'''

from tentacleexplorer import TentacleExplorer

import math
import MapTools as tools

UNKNOWN = 127
FREE = 255
WALL = 0

class Position():

    
    def __init__(self, x_pixels, y_pixels, mapbytes, map_size, tentacles, max_search, min_dist):
        self.x_pixels = x_pixels
        self.y_pixels = y_pixels
        self.explorer = TentacleExplorer(x_pixels, y_pixels, map_size)
        self.updateTargets(mapbytes, map_size, tentacles, max_search)


    def updateTargets(self, mapbytes, map_size, tentacles, max_search, min_dist):
        """
        creates a queue of targets
        """
        angleDif = math.pi * 2 / tentacles
        values = []
        for a in range(0, tentacles):
            angle = a * angleDif
            dx = math.cos(angle)
            dy = math.sin(angle)
            values.append(getTentacleValue(mapbytes, mapsize, dx, dy, max_search, min_dist))

        frontiers[]
        current = None
        for i in range(0, len(values)):
            if(values[i] == UNKOWN):
                if(current == None):
                    current = [values[i]]
                else:
                    current.append(values[i])
            else:
                if(current != None):
                    frontiers.append(current)
                    current = None

        if(len(frontiers)==0):
            return []
        if(len(frontiers>
            
                          

    def getTentacleValue(self, mapbytes, mapsize, dx, dy, max_dist, min_dist):
        """
        find tentacle value
        """
        #make value iteratable
        if(math.fabs(dx)>math.fabs(dy)):
            dx = float(dx)/dy
            dy = 1
        else:
            dy = float(dy)/dx
            dx =1
        step_dist = math.sqrt(dx*dx+dy*dy)
        steps = int(max_dist/step_dist)
        start = int(min_dist/step_dist)
        for i in range(start,steps):
            x = dx*i + self.x_pixels
            y = dy*i + self.y_pixels
            value = tools.getValue(x, y, mapbytes, self.mapsize)
            if(value == UNKNOWN): return (x,y, unknown)
            if(value != FREE): return (x, y, WALL)
                
        return FREE

    def getPosition(self):
        return (self.x_pixels, self.y_pixels)
        
    
    def getNextTarget(self):
        '''
        Return then next best target. Or null if there is none anymore
        '''
        if(len(self.targets) == 0): return None
        return self.targets.popleft()
       
