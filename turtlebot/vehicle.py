'''
vehilce.py: base class for any vehicle like turtlebot
             
author: Nils Bernhardt 
'''

import abc


class Vehicle(object):

    @abc.abstractmethod
    def get_odometry(self):
        """Return a tuple of odometry (dxy in mm,dthata in degree, dt in s)"""
        return

    @abc.abstractmethod
    def initialize(self):
        """Prepare"""
        return

    @abc.abstractmethod
    def shutdown(self):
        """Stop every running thread"""
        return

    @abc.abstractmethod
    def move(self, cmd):
        """
        Move by dxy millimeters
        :param cmd: Command.
        """
        return

    @abc.abstractmethod
    def getSize(self):
        """Return size in meter"""
        return

