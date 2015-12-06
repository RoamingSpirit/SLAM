__author__ = 'troyhughes'


from PathPlanningInterface import PPI
import Queue

class aStarPlanner(PPI):

    def __init__(self,mapconf, min_dist):
        self.mapconf = mapconf
        self.min_dist = min_dist


    def makePath(self, position, mapbytes, goal):
        """

        :param position: (x,y,theta) touple of the position of the robot
        :param mapbytes: version of the map
        :param goal: (x,y) touple of the goal
        :return: list of touples that the system can travel to
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

            nodeNeighbors = self.mapconf.getNeighbors(nodeX, nodeY, mapbytes,FOUR_EXPAND)
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
        :param astarDict : dictionary search tree being stored as to,from as key,value. Therefore can recreate the path by using the goal.
        :param goal : the goal location of the robot
        :return: list of points (x,y touples) that is the path to take to the goal
        """
        path = [goal]                      ## Initialize path

        ## Prime the statements for iterating to the end of the path
        current_location = goal
        prev = astarDict[current_location]
        path.insert(0,prev)
        current_location = prev

        ## Traverse the tree from leaves to trunk
        while prev is not None:
            prev = astarDict[current_location]
            if prev is None:
                continue
            path.insert(0,prev)
            current_location = prev

        return path



