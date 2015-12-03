__author__ = 'troyhughes'

import abc

class FEI(object):

    @abc.abstractmethod
    def expandObstacles(self):
        pass

    @abc.abstractmethod
    def findFrontiers(self):
        pass
