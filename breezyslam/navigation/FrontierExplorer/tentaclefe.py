'''

             
author: Nils Bernhardt 
'''

from FrontierExplorerInterface import FEI

from Queue import PriorityQueue

import math



class TentacleFE(FEI):

    
    def __init__(self, mapconf, tentacles, max_search, min_dist):
        self.mapconf = mapconf
        self.tentacles = tentacles
        self.max_search = max_search
        self.min_dist = min_dist


    def findFrontiers(self, position, mapbytes, width):
        """
        return a priority queue with coordinates (x_pixels, y_pixels)
        """
        return self.getTargets(position[0], position[1], mapbytes, self.mapconf.SIZE_PIXELS, self.tentacles, self.max_search, self.min_dist)

    def getTargets(self, x, y, mapbytes, map_size, tentacles, max_search, min_dist):
        """
        creates a queue of targets
        """
        angleDif = math.pi * 2 / tentacles
        values = []
        for a in range(0, tentacles):
            angle = a * angleDif
            dx = math.cos(angle)
            dy = math.sin(angle)
            values.append(self.getTentacleValue(x, y, mapbytes, map_size, dx, dy, max_search, min_dist))

        frontiers = PriorityQueue()
        current = None
        maxPos = tentacles/4
        for i in range(0, len(values)):
            if(values[i][2] == self.mapconf.UNKNOWN):
                if(current == None):
                    current = [values[i]]
                elif(len(current) < maxPos):
                    current.append(values[i])
                else:
                    frontiers.put((len(current), self.getCenter(current)))
                    current = None
            else:
                if(current != None):
                    frontiers.put((len(current), self.getCenter(current)))
                    current = None
        
        return frontiers

    def getCenter(self, positions):
        x = 0
        y = 0
        for pos in positions:
            x += positions[0]
            y += positions[1]
        return (x/len(positions), y/len(positions))
            
                          

    def getTentacleValue(self, xc, yc, mapbytes, mapsize, dx, dy, max_dist, min_dist):
        """
        find tentacle value
        """
        #make value iteratable
        if(math.fabs(dx)>math.fabs(dy)):
            if(dy == 0):
                dx = 1
            else:
                dx = float(dx)/dy
                dy = 1
        else:
            if(dx==0):
                dy=1
            else:
                dy = float(dy)/dx
                dx =1
        step_dist = math.sqrt(dx*dx+dy*dy)
        steps = int(max_dist/step_dist)
        start = int(min_dist/step_dist)
        for i in range(start,steps):
            x = dx*i + xc
            y = dy*i + yc
            value = self.mapconf.getValue(x, y, mapbytes, self.mapsize)
            if(value == self.mapconf.UNKNOWN): return (x,y, self.mapconf.UNKNOWN)
            if(value != self.mapconf.FREE): return (x, y, self.mapconf.WALL)
                
        return (xc, yc, self.mapconf.FREE)

