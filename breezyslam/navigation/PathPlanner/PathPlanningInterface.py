__author__ = 'troyhughes'


import abc

class PPI(object):

    @abc.abstractmethod
    def makePath(self, position, mapbytes, goal):
        """

        :param position: (x,y,theta) touple of the position of the robot
        :param mapbytes: version of the map
        :param goal: (x,y) touple of the goal
        :return: list of touples that the system can travel to
        """
        pass

