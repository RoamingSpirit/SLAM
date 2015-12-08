from vehicle import Vehicle
from RS_Turtlebot import ros_turtlebot

import time
import rospy
import math



class Turtlebot(Vehicle, ros_turtlebot.ROSTurtlebot):


    def __init__(self):
        """
        This will handle all of the initialization information for the turtlebot
        :param COMPort: String rep of the serial port to communicate on.
        :return:
        """
        self._past_x = None
        self._past_y = None
        self._past_theta = None

        self._d_theta = None
        self._d_traveled = None
        self._start = True

        self._diffx = None
        self._diffy = None
        self._difftheta = None
        self._time = time.time()
        self.initialize()


        # self._com = SCommunicator.SCommunicator(COMPort)
        print "Turtlebot Initialization Complete"

    def initialize(self):
        ros_turtlebot.ROSTurtlebot.__init__(self)

        if self._past_x is not None and self._past_y is not None and self._past_theta is not None:
            print "Turtlebot properly instantiated subclass"
        else:
            print self._past_x, self._past_y, self._past_theta
            raise NotImplementedError("Turtlebot Subclass not properly instantiated")
        return

    def getOdometry(self):
        """
        This will run the serial commands to send the odom data. the _getOdomROS function will calculate
        and store the difference between the last time it was called and now.
        :return: (dxy in mm, dtheta in degrees, time difference)
        """

        self.odom_lock.acquire()
        response = (self._accumXY*1000,self._accumT,time.time() - self._time)
        self._accumXY = 0
        self._accumT = 0
        self.odom_lock.release()

        self._time = time.time()
        return response
    

    def shutdown(self):
        """stop every running thread"""
        return

    def move(self, dxy):
        """move by dxy Millimeters"""
        self._driveStraight(0.5, dxy/1000)


    def turn(self, dtheta):
        """ Move by dtheta degrees"""
        self._rotate(dtheta, 0.5)
        return
