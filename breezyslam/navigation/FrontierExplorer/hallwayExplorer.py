__author__ = 'troyhughes'


from FrontierExplorerInterface import FEI
import MapTools as MT
import Queue



class HallwayExplorer(FEI):


    def __init__(self, MAP_CODE_TOUPLE, MAP_SIZE_PIXELS, MAP_SIZE_METERS, ROBOT_SIZE_METERS):
        self._WALL, self._UNK, self._OPN = MAP_CODE_TOUPLE
        self._MAP_SIZE_PIXELS = MAP_SIZE_PIXELS
        self._MAP_SIZE_METERS = MAP_SIZE_METERS
        self._ROBOT_SIZE_METERS = ROBOT_SIZE_METERS

        #TODO : Implement functions to translate the map to pixles or mm
        #TODO : Implement function to easily reference pixles from the map
        #TODO : Implement the searching algorithm to fill a list of the frontiers
        #TODO : Priority queue the list based off closeness to the robot
        #TODO : implement get neighbor functions < Located in the MapTools.py File >
        #TODO : What is position in these? A x and y location? DOes it include direction?

        ## TODO : What are the dimensions of the map in terms of pixles or mm or? pixels


    def expandObstacles(self, position, mapbytes):
        """
        Expand the obstacles in the map by half the size of the robot so that the
        navigation algorithms will never contact the obsticals

        :param position: x_mm, y_mm touple
        :param mapbytes: 1d representation of a 2d map in #TODO : What are the dimensions of the map?
        :return:
        """
        return


    def findFrontiers(self, position, mapbytes, width):
        frontiers = Queue.PriorityQueue()
        cx,cy = position   # Get the current x and y of the robot from the position touple
        hallwayExpand = MT.getNeighbors(cx,cy,mapbytes,width,FOUR_EXPAND = False)

        for square in hallwayExpand:
            x,y,v = square

            ## Find the differnce betwen the x and y to know what the incremental direction is
            ## ## and then add the current x and y to it to get x back
            newx = (x - cx) + cx
            newy = (y - cy) + cy
            counter = 1

            while v != self._WALL or v != self._UNK:
                if MT.outofBounds(newx,newy,width):
                    raise RuntimeError("Edge of map detected in findFrontiers")
                v = MT.getValue(newx, newy, mapbytes, width)
                newx = (x - cx) + newx
                newy = (y - cy) + newy
                counter = counter + 1


            if v == self._UNK:
                frontiers.put((counter,(newx,newy)))

        return frontiers


    """
        Thoughts:
            We could do a 'hallway classifier' algorithm that expands 8 ways out to find walls and
            unknown regions and then use those lists to expand from there
    """


