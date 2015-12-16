'''

             
author: Nils Bernhardt 
'''

from FrontierExplorerInterface import FEI

from Queue import PriorityQueue

import math

#minimum amount of valid tentacles to form a frontier
MINIMUM_TENTACLES = 5 



class TentacleFE(FEI):
    
    def __init__(self, mapconf, tentacles, min_dist, max_search):
        self.mapconf = mapconf
        self.tentacles = tentacles * 3
        self.max_search = max_search
        self.min_dist = min_dist
        #print "Tentacle Fe initialized with %d tentacles and dist between %d and %d" % (tentacles, min_dist, max_search) 

    def findFrontiers(self, position, mapbytes, width):
        """
        return a priority queue with coordinates (x_pixels, y_pixels)
        """
        #print "Finding frontiers at %f|%f" %(position)
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
            #print "Tentacle #%d with angle %f on vector %f|%f" %(a, angle,dx,dy)
            value = self.getTentacleValue(x, y, mapbytes, map_size, dx, dy, max_search, min_dist)
            #print "Tentacle value at %f|%f is %d" % value
            values.append(value)

        frontiers = PriorityQueue()
        current = None
        maxPos = tentacles/4
        for i in range(0, len(values)):

            ##debug only remove later
            #self.mapconf.drawRect(values[i][0], values[i][1], 5, 0, mapbytes)

            if(values[i][2] == self.mapconf.UNKNOWN):
                if(current == None):
                    #print "New forntier"
                    current = [values[i]]
                elif(len(current) < maxPos):
                    #print "Adding frontier"
                    current.append(values[i])
                else:
                    #print "max size reached. Storing"
                    frontiers.put((-len(current), self.getCenter(current)))
                    current = [values[i]]
            else:
                if(current != None):
                    #print "End reached. Storing."
                    if(len(current) > MINIMUM_TENTACLES and self.getFrontierLength(current) > self.min_dist):
                        frontiers.put((-len(current), self.getCenter(current)))
                    current = None


        return frontiers

    def getFrontierLength(self, frontier):
        x1 = frontier[0][0]
        y1 = frontier[0][1]
        x2 = frontier[len(frontier)-1][0]
        y2 = frontier[len(frontier)-1][1]
        dx = x1-x2
        dy = y1-y2
        return math.sqrt(dx*dx+dy*dy)
            

    def getCenter(self, positions):
        x = 0
        y = 0
        for pos in positions:
            x += pos[0]
            y += pos[1]
        return (x/len(positions), y/len(positions))

    def getTentacleValue(self, xc, yc, mapbytes, mapsize, dx, dy, max_dist, min_dist):
        """
        find tentacle value
        """
        #make value iteratable
        if(math.fabs(dx)>math.fabs(dy)):
            dy = float(dy)/math.fabs(dx)
            if(dx>0): dx = 1
            else: dx = -1
        else:
            dx = float(dx)/math.fabs(dy)
            if(dy>0): dy = 1
            else: dy = -1
        #print "corrected vector %f|%f" %(dx,dy)
        step_dist = math.sqrt(dx*dx+dy*dy)
        steps = int(max_dist/step_dist)
        start = int(min_dist/step_dist)
        #print "searching between %d and %d with %f stepsize" %(start, steps, step_dist)
       
        for i in range(start,steps):
            x = int(dx*i + xc)
            y = int(dy*i + yc)
            value = self.mapconf.getValue(x, y, mapbytes)
            if(value == self.mapconf.UNKNOWN): return (x,y, self.mapconf.UNKNOWN)
            #if(value != self.mapconf.FREE): return (x, y, self.mapconf.WALL)
            if(value < self.mapconf.UNKNOWN): return (x, y, self.mapconf.WALL)
           
        return (x, y, self.mapconf.FREE)

