__author__ = 'troyhughes'

from FrontierExplorerInterface import FEI
import MapTools as MT


class bfsFE(FEI):


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

        ## TODO : What are the dimensions of the map in terms of pixles or mm or?


    def expandObstacles(self, position, mapbytes):
        """
        Expand the obstacles in the map by half the size of the robot so that the
        navigation algorithms will never contact the obsticals

        :param position: x_mm, y_mm touple
        :param mapbytes: 1d representation of a 2d map in #TODO : What are the dimensions of the map?
        :return:
        """
        return


    def findFrontiers(self):
        return


