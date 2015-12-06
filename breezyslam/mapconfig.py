import math


class MapConfig():

    SIZE_PIXELS = 1000
    SIZE_METERS = 40

    UNKNOWN = 127
    FREE = 255
    WALL = 0
    
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
        return not (x >= self.SIZE_PIXELS or y >= self.SIZE_PIXELS or x < 0 or y < 0)

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