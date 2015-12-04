__author__ = 'troyhughes'


from PathPlanningInterface import PPI

class aStarPlanner(PPI):

    def __init__(self,mapconf, min_dist):
        self.mapconf = mapconf
        self.min_dist = min_dist


    def makePath(self, position, mapbytes, goal):
        """
        This returns a path from position to goal (within a min_dist) safety factor.

        :param position:
        :param mapbytes:
        :param goal:
        :return:
        """
        aStarSearchTree = self._astar(position, mapbytes, goal)
        path = self._pathFromDict(aStarSearchTree, goal)

        return path

    def _astar(self,position,mapbytes,goal):
        """

        :param position: (x,y,theta) touple
        :param mapbytes: the map object
        :param goal: (x,y) touple of the goal
        :return: dictionary representing the search tree
        """

        return

    def _pathFromDict(self, astarDict, goal):
        return


    def _getNeighbors(self, x,y,map, FOUR_EXPAND=True):
        # def getNeighbors(x, y, map, width, FOUR_EXPAND):
        if map is None:
            raise RuntimeError("Map is none")

        four_expand = [(x+1,y),
                       (x-1,y),
                       (x,y+1),
                       (x,y-1)]
        eight_expand = []; eight_expand.extend(four_expand)
        eight_expand.extend([(x+1,y+1),
                             (x+1,y-1),
                             (x-1,y-1),
                             (x-1,y+1)])
        ret_list = []
        num_expand = []
        ## Pick how many surrounding nodes to expand
        if FOUR_EXPAND: num_expand.extend(four_expand)
        else: num_expand.extend(eight_expand)

        for v in num_expand:
            try:
                tx,ty = v
                ## Screen out the values that are out of bounds
                if self.mapconf.outofBounds(tx,ty):
                    continue
                inbound_value = self.mapconf.getValue(x,y,map)
                ret_list.append((tx,ty,inbound_value))

            except Exception,e:
                print "Something else has errored in 'getNeighhbors'"
                raise e


        return ret_list