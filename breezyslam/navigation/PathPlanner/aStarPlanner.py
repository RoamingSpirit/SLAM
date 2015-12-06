__author__ = 'troyhughes'


from PathPlanningInterface import PPI
import Queue

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

    def _astar(self,position,mapbytes,goal,heuristic, FOUR_EXPAND):
        """

        :param position: (x,y,theta) touple
        :param mapbytes: the map object
        :param goal: (x,y) touple of the goal
        :param heuristic: Function that takes (goal<touple>, point<touple>) and returns a heuristic cost between the two
        :return: dictionary representing the search tree
        """
        sx,sy,st = position
        goalX, goalY = goal

        frontier = Queue.PriorityQueue()
        frontier.put((0,(sx,sy)))

        came_from = {(sx,sy):None}
        cost_so_far = {(sx,sy):0}

        while not frontier.empty():
            current_priority_touple = frontier.get()
            _,current_node = current_priority_touple
            nodeX,nodeY = current_node

            if nodeX == goalX and nodeY == goalY:
                break

            nodeNeighbors = self._getNeighbors(nodeX, nodeY, mapbytes,FOUR_EXPAND=FOUR_EXPAND)
            for next in nodeNeighbors:
                nextStepCost = cost_so_far[current_node] + self.mapconf.costTravel(current_node, next)
                if next not in cost_so_far or nextStepCost < cost_so_far[next]:
                    cost_so_far[next] = nextStepCost
                    nextStepPriority = nextStepCost + heuristic(current_node, next)
                    frontier.put((nextStepPriority,next))
                    came_from[next] = current_node

        return came_from

    def _pathFromDict(self, astarDict, goal):
        """
        This function uses A* to generate a from start to end and then returns it.
        :param start:
        :return: list of points (x,y touples) that is the path to take to the goal
        """
        path = [goal]                      ## Initialize path

        ## Prime the statements for iterating to the end of the path
        current_location = goal
        prev = astarDict[current_location]
        path.append(prev)
        current_location = prev

        ## TODO: Make this so it adds to the start of th elist not the end.
        ## Traverse the tree from leaves to trunk
        while prev is not None:
            prev = astarDict[current_location]
            if prev is None:
                continue
            path.append(prev)
            current_location = prev

        path.reverse()                              ## Reverse the list so it goes from start to finish

        return path



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