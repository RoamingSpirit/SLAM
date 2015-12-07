__author__ = 'troyhughes'


from FrontierExplorerInterface import FEI
import Queue



class HallwayExplorer(FEI):
    divList = [8,40]

    def __init__(self, mapconf, numDivisions):
        self._setDiv(numDivisions)
        self.mapconf = mapconf


        #TODO : Implement functions to translate the map to pixles or mm
        #TODO : Implement function to easily reference pixles from the map
        #TODO : Implement the searching algorithm to fill a list of the frontiers
        #TODO : Priority queue the list based off closeness to the robot
        #TODO : implement get neighbor functions < Located in the MapTools.py File >
        #TODO : What is position in these? A x and y location? DOes it include direction?

        ## TODO : What are the dimensions of the map in terms of pixles or mm or? pixels

    def _setDiv(self, numDivisions):
        ## Set the number of divisions for the map to be divided
        if numDivisions > len(self.divList):self.div = self.divList[-1]
        elif numDivisions < 0: self.div = self.divList[0]
        else: self.div = self.divList[numDivisions]


    def expandObstacles(self, position, mapbytes):
        """
        Expand the obstacles in the map by half the size of the robot so that the
        navigation algorithms will never contact the obsticals

        :param position: x_mm, y_mm touple
        :param mapbytes: 1d representation of a 2d map in #TODO : What are the dimensions of the map?
        :return:
        """
        wall_list = self.divideFind(mapbytes)
        wall_list = self.mapconf.likeNeighbors(wall_list,self.mapconf.WALL, mapbytes)

        for wall in wall_list:
            self.mapconf.dialateNode(wall,mapbytes)

        return mapbytes


    def divideFind(self, mapbytes):
        smallImageSize = self.mapconf.SIZE_PIXELS/self.div
        ## TODO : Ensure that the difVlist guarentees odd size
        ## Because the image is an odd size (guarenteed by divList set) we can find the guarenteed center
        cntr = ((smallImageSize - 1)/2) + 1
        pointList = []

        for y in xrange(self.div):
            for x in xrange(self.div):
                pointList.append((x*smallImageSize + cntr,y*smallImageSize + cntr))
        wall_list = []

        for point in pointList:
            x,y = point
            val = self.mapconf.getValue(x, y, mapbytes)
            if val == self.mapconf.WALL:
                wall_list.append(point)

        return wall_list

    def findFrontiers(self, position, mapbytes, width):
        frontiers = Queue.PriorityQueue()
        cx,cy = position   # Get the current x and y of the robot from the position touple
        hallwayExpand = self.mapconf.getNeighbors(cx,cy,mapbytes,width,FOUR_EXPAND = False)

        for square in hallwayExpand:
            x,y,v = square

            ## Find the differnce betwen the x and y to know what the incremental direction is
            ## ## and then add the current x and y to it to get x back
            newx = (x - cx) + cx
            newy = (y - cy) + cy
            counter = 1

            while (v != self.mapconf.WALL or v != self.mapconf.WALL) and \
                    not (self.mapconf.outofBounds(newx,newy,width)):
                v = self.mapconf.getValue(newx, newy, mapbytes, width)
                newx = (x - cx) + newx
                newy = (y - cy) + newy
                counter = counter + 1


            if v == self.mapconf.UNKNONW:
                frontiers.put((counter,(newx,newy)))

        return frontiers



