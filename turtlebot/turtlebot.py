from vehicle import Vehicle
from RS_Turtlebot import ros_turtlebot
import time
import rospy
import math


class Turtlebot(Vehicle, ros_turtlebot.ROSTurtlebot):
    SPEED = 0.5

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

    def get_odometry(self):
        """

        This will run the serial commands to send the odom data. the _getOdomROS function will calculate
        and store the difference between the last time it was called and now.

        :return: (dxy in mm, dtheta in degrees, time difference)
        """
        if self._start:
            dxy = math.sqrt(self._past_x ** 2 + self._past_y ** 2)
            dtheta = self._past_theta
        else:
            dxy = math.sqrt((self._diffx - self._past_x) ** 2 + (self._diffy - self._past_y) ** 2)
            dtheta = self._difftheta - self._past_theta

        response = (dxy * 1000, dtheta, time.time() - self._time)

        self._diffx = self._past_x
        self._diffy = self._past_y
        self._difftheta = self._past_theta
        self._time = time.time()
        return "%f,%f,%f" % response

    def shutdown(self):
        """
        Stop every running thread.
        """
        self._stopRobot()
        return

    def move(self, command):
        """
        Move the TurtleBot.
        :param command: Move command.
        """
        if command == 2:
            # Move forward.
            self._stopRobot()
            self._driveStraight(Turtlebot.SPEED)
        elif command == 3:
            # Turn right.
            self._stopRobot()
            self._rotate(Turtlebot.SPEED)
        elif command == 4:
            # Turn left.
            self._stopRobot()
            self._rotate(-Turtlebot.SPEED)
        elif command == 5:
            # Wait.
            self._stopRobot()
