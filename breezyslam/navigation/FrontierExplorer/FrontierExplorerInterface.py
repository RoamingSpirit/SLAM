__author__ = 'troyhughes'

import abc

class FEI(object):

    @abc.abstractmethod
    def __init__(self, MAP_CODE_TOUPLE):
        pass

    @abc.abstractmethod
    def expandObstacles(self, position, mapbytes):
        """
        This should return an updated mapbytes
        :param position:
        :param mapbytes:
        :return:
        """
        pass

    @abc.abstractmethod
    def findFrontiers(self, position, mapbytes, width):
        """
        return a priority queue with coordinates (x_pixels, y_pixels)
        """
        pass
