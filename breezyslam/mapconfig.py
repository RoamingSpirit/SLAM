import math
from PIL import Image

class MapConfig():

    UNKNOWN = 127
    FREE = 255
    WALL = 0

    def __init__(self, SIZE_PIXELS = 1000, SIZE_METERS = 40):
        self.SIZE_PIXELS = SIZE_PIXELS
        self.SIZE_METERS = SIZE_METERS

    def safeaspng(self, mapbytes, filename):
        im = Image.new('L', (1000,1000))
        im.putdata(mapbytes)
        im.save(filename)
    
    def getValue(self,x, y, mapbytes):
        """
        get the value at the x,y location of a 1d rep of a 2d map
        :param x: x location
        :param y: y location
        :param map: 1 dimensional rep of a 2d map
        :param width: width of the 2d map
        :return: value at the x,y location
        """
        return mapbytes[y*self.SIZE_PIXELS+x]

    def setValue(self,x, y, value, mapbytes):
        """
        Set the value at x,y on a arrayList map
        :param x: x location
        :param y: Y location
        :param value: Value to set
        :param map: 1 dimensional representation of a 2d map
        :param width: width of the 2 dimensional map
        :return: 1d rep of the 2d map with the change.
        """
        mapbytes[y*self.SIZE_PIXELS+x] = value
        return mapbytes

    def mmToPixels(self, value):
        return self.SIZE_PIXELS/(self.SIZE_METERS*1000.0)*value

    def mToPixels(self, value):
        return float(self.SIZE_PIXELS)/self.SIZE_METERS*value
    
    def pixelsTomm(self, value):
        return (self.SIZE_METERS*1000.0)/self.SIZE_PIXELS*value

    def outofBounds(self, x,y):
        """
        Returns True if the value is out of bounds of a specific map

        :param x: x location
        :param y: y location
        :return: boolean representing if the value is out of bounds or not
        """
        return (x >= self.SIZE_PIXELS or y >= self.SIZE_PIXELS or x < 0 or y < 0)

    def costTravel(self, start, goal):
        """
        Calculates the cost of travel from one node to the next.

        :param start: (x,y) touple
        :param goal: (x,y) touple
        :return:
        """

        x1, y1 = start
        x2, y2 = goal

        return math.sqrt((x1-x2)**2 + (y1-y2)**2)


    def dialateNode(self,node, map):
            """
            This dialates one node on a map and returns the map.
            :param map: A list of lists of intigers with min 0 and max 100
            :param node: x,y tuple of the location
            :param max_x: width of the map
            :param max_y: height of the map
            :return:
            """
            x,y = node
            gen_neighbors = [(x-1,y-1),             ## All possible neighbors
                             (x+1,y+1),
                             (x+1,y-1),
                             (x-1,y+1),
                             (x,y+1),
                             (x,y-1),
                             (x-1,y),
                             (x+1,y)]

            for n in gen_neighbors:
                nx,ny = n
                if not self.outofBounds(nx,ny):
                    self.setValue(nx,ny,self.WALL,map)
            return map


    def likeNeighbors(self, listOfPoints, pointValue, mapbytes):
        """
        This function returns a list of the surrounding points that are the same as the pointValue passed. The points are
        found as surrounding on the mapbytes map

        :param listOfPoints: list of (x,y) touples that represent the the points to search
        :param pointValue: INT :: This is the value of the neighbors that we want
        :param mapbytes: This is the 1d rep of the 2d map
        :return: list of (x,y) touples that including the listOfPoints passed.
        """
        ERRROR = True
        if not ERRROR:

            FOUR_EXPAND = "[(x+1,y), (x-1,y), (x,y+1), (x,y-1)]"
            neighborlist = set()
            to_explore_list = set()
            for point in listOfPoints:
                x,y = point
                gettingNeighbors = True
                for neighbor in self.getNeighbors(x,y,mapbytes,FOUR_EXPAND):   ## 4 expanding for now.
                    nx,ny = neighbor
                    if self.getValue(nx,ny,mapbytes) == self.WALL:
                        to_explore_list.add(neighbor)
                        neighborlist.add(neighbor)

                ## TODO : Fix this code, set cannot change size while iterating over it.
                """ It might be a smart idea to write your own 'set' class or something. Something that can be mutated
                while you're for looping over it or something. Idk, we just need to make sure that we expand all of like
                neighbors around a certain point. The point of this is to expand obstacles... """
                while gettingNeighbors:
                    for node in to_explore_list:
                        nx,ny = node
                        nodeNeighbors = self.getNeighbors(nx,ny,mapbytes,FOUR_EXPAND)
                        for neighbor in nodeNeighbors:
                            nnx,nny = neighbor
                            if self.getValue(nnx,nny,mapbytes) == self.WALL:
                                to_explore_list.add(neighbor)
                                neighborlist.add(neighbor)
        else:
            raise  NotImplementedError("likeNeighbors not implemented")





    def getNeighbors(self, x,y,map, neighborlist):
        """
        This returns the neighbors around the x and y locaiton on a map. the neighbors explored are by the neighborslist
        that is passed in the arguments.

        :param x: x location of the robot
        :param y: y location of the robot
        :param map: this is the map that the robot exsists in
        :param neighborlist: a string representation of a list that can be eval'ed. Should be of the form: "[(),(),()...]"
        :return: Dictionary of the search tree.
        """

        neighborlist = eval(neighborlist)

        if map is None:
            raise RuntimeError("Map is none")

        ret_list = []
        for neighbor in neighborlist:
            try:
                tx,ty = neighbor
                ## Screen out the values that are out of bounds
                if self.outofBounds(tx,ty):
                    continue
                inbound_value = self.getValue(x,y,map)
                ret_list.append((tx,ty,inbound_value))

            except Exception,e:
                print "Something else has errored in 'getNeighhbors'"
                raise e

        return ret_list

    def drawCross(self, xc, yc, size, value, mapbytes):
        xc = int(xc)
        yc = int(yc)
        for i in range(-size/2, size/2):
            x = i + xc
            y = i + yc
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)

        for i in range(-size/2, size/2):
            x = i + xc
            y = yc - i
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)

    def drawPlus(self, xc, yc, size, value, mapbytes):
        xc = int(xc)
        yc = int(yc)
        y = yc
        for x in range(xc-size/2, xc+size/2):
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)

        x = xc
        for y in range(yc-size/2, yc+size/2):
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)

    def drawRect(self, xc, yc, size, value, mapbytes):
        xc = int(xc)
        yc = int(yc)
        for x in range(xc-size/2, xc+size/2):
            y = yc+size/2
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)
            y = yc-size/2
            if not self.outofBounds(x, y):
                    self.setValue(x, y, value, mapbytes)

        for y in range(yc-size/2, yc+size/2):
            x = xc+size/2
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)
            x = xc-size/2
            if not self.outofBounds(x, y):
                self.setValue(x, y, value, mapbytes)



