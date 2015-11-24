'''
vehilce.py: base class for any vehicle like turtlebot
             
author: Nils Bernhardt 
'''

import abc

class Vehicle(object):

    @abc.abstractmethod
    def getOdometry(self):
        """return a tuple of odometry (dxy in mm,dthata in degree, dt in s)"""
        return

    @abc.abstractmethod
    def initialize(self):
        """prepare"""
        return

    @abc.abstractmethod
    def shutdown(self):
        """stop every running thread"""
        return

    @abc.abstractmethod
    def move(self, dxy):
        """move by dxy milimeters"""
        return

    @abc.abstractmethod
    def turn(self, dtheta):
        """turn by dtheta degrees (clockwise)"""
        return
