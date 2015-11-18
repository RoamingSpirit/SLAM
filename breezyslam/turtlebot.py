from vehicle import Vehicle
from CPI_Protocol import SCommunicator
from RS_Turtlebot import ros_turtlebot

import rospy




class Turtlebot(Vehicle, ros_turtlebot.ROSTurtlebot):
    def __init__(self,COMPort):
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

    def _publishTwist(self,u,v):
        """
        Publish a twist message to ROS

        :param u: Linear Velocity
        :param v: Angular Velocity
        :return:None
        """
        ros_turtlebot.ROSTurtlebot._spinWheels(self,u,v,self._pub)
        return

    def getOdometry(self):
        """

        This will run the serial commands to send the odom data. the _getOdomROS function will calculate
        and store the difference between the last time it was called and now.

        :return: Will return nothing, instead published to the serial port.
        """
        print ("Odom is: ",self._d_traveled*100, self._d_theta)
        return

    def shutdown(self):
        """stop every running thread"""
        self._com.close()
        return

    def move(self, dxy):
        """move by dxy milimeters"""
        self._driveStraight(0.5, dxy/100)


    def turn(self, dtheta):
        """ Move by dtheta degrees"""
        self._rotate(0.5, dtheta)
        return


turtle = Turtlebot("SomePort")
while not rospy.is_shutdown():
    turtle.getOdometry()
    rospy.sleep(0.1)

