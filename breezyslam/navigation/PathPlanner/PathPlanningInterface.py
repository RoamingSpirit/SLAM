__author__ = 'troyhughes'


import abc

class PPI(object):

    FOUR_EXPAND = "[(x+1,y), (x-1,y), (x,y+1), (x,y-1)]"
    EIGHT_EXPAND = "[(x+1,y), (x-1,y), (x,y+1), (x,y-1), (x+1,y+1), (x+1,y-1), (x-1,y-1), (x-1,y+1)]"

    @abc.abstractmethod
    def makePath(self, position, mapbytes, goal):
        """

        :param position: (x,y,theta) touple of the position of the robot
        :param mapbytes: version of the map
        :param goal: (x,y) touple of the goal
        :return: list of touples that the system can travel to
        """
        pass

