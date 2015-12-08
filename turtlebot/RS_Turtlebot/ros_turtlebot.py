__author__ = 'Troy Hughes'

#Imports
import rospy
import roslib

import time
import math
import tf
import serial

""" The below imports are dependant on ROS being installed an the enclosing folder being
    a catkin workspace/catkin_package. Without these, the program will not be able to run"""
#Message Types
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import PoseStamped

from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
from kobuki_msgs.msg import BumperEvent

import threading

class ROSTurtlebot(object):
    #odom_lock = threading.Condition()

    def __init__(self):
        rospy.init_node("Roaming_Spirit_Odom")
        self._sub = rospy.Subscriber('/odom', Odometry, self._getOdomROS, queue_size=3)
        self._pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)

        self._odom_list = tf.TransformListener()
        self._odom_tf = tf.TransformBroadcaster()
        self._past_x = 0; self._past_y = 0; self._past_theta = 0;

        self._odom_tf.sendTransform((0, 0, 0),
                                    (0, 0, 0, 1),
                                    rospy.Time.now(),
                                    "base_footprint","odom")

        self._wheelbase = 0.352
        self._past_x =0.0
        self._past_y = 0.0
        self._past_theta = 0.0

        self._d_theta = None
        self._d_traveled = None


        #threading.Thread.__init__(self)
        self._accumXY = 0.0
        self._accumT = 0.0


        sleeper = rospy.Duration(1)
        rospy.sleep(sleeper)
        print "Subclass Instantiated"


    def _getOdomROS(self, msg):
        """
        This function is the ROS callback that allows the turtlebot script to know what the odometry data is for the
        turtlebot it is attached to

        :param msg: This is the message that the robot receives from listening to the '/odom' topic
        :return: None
        """


        # Find the distance traveled
        self._d_traveled = math.sqrt((self._past_x - msg.pose.pose.position.x)**2 +
                               (self._past_y - msg.pose.pose.position.y)**2)

        self._quat = (msg.pose.pose.orientation.x,
                msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z,
                msg.pose.pose.orientation.w)

        current_theta_rad = self._normalizeTheta(self._quat)

        # Calculates the difference in the thetas
        if self._past_theta > current_theta_rad and self._past_theta > math.pi*3/2 and current_theta_rad < math.pi/2:
            self._d_theta = ((2*math.pi) - self._past_theta) + current_theta_rad
        elif self._past_theta < current_theta_rad and self._past_theta < math.pi/2 and current_theta_rad > math.pi*3/2:
            self._d_theta = ((2*math.pi) - current_theta_rad) + self._past_theta
        else:
            self._d_theta = self._past_theta - current_theta_rad

        # Store for next calculation
        self._past_x = msg.pose.pose.position.x
        self._past_y = msg.pose.pose.position.y
        self._past_theta = current_theta_rad

        #self.odom_lock.acquire()
        #Fill the accumulator variabnles:
        self._accumXY = self._accumXY + self._d_traveled
        self._accumT = self._accumT + self._d_theta
        #self.odom_lock.release()


    def _publishTwist(self, u, w, publisher):
        """
        This function creates a twist message to give to the publisher to publish

        :param u: linear velocity
        :param w: angular velocity
        :param publisher: The publisher to send it to the topic
        :return:
        """

        twist = Twist()
        twist.linear.x = u; twist.angular.z = w

        twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0

        publisher.publish(twist)

    def _spinWheels(self, u1, u2):
        """
        This will spin the left wheel u1 and the right wheel u2 for timesec <seconds>

        :param u1: left Wheel velocity
        :param u2: Right Wheel Velocity
        :param timesec: How long this will happen for
        :return: None
        """
        lin_vel = (0.5)*(u1 + u2)
        ang_vel = (1/(self._wheelbase))*(u1-u2)

        self._publishTwist(lin_vel, ang_vel, self._pub)
        
        return


    def _stopRobot(self):
        """  Publishes a stop message to the robot
        :return:None
        """
        self._publishTwist(0,0, self._pub)

    def _driveStraight(self, speed):
        """
        THis takes in a speed and distance and moves in the facing direction
        until it has reached the distance.

        NOTE: This function denotes it's travel by how far the 'odom' frame believes
        it has traveled. NOT how far it has traveled in the /map.

        :param speed: This is a 0 to 1 value, it will cap the values at 1 and 0.
        :param distance: This is a value in meters.
        :return: Nothing
        """
        self._spinWheels(speed, speed)

    def _rotate(self, speed = 0.05):
        """
        :param angle: <int or double> the angle the robot should turn in degrees
        :param speed: <int or double> The speed at which the robot should rotate
        :return: None
        """
        self._spinWheels(speed,-speed)


    def _normalizeTheta(self, quaternian_touple):
        """
        This takes in a quaternian touple and returns a 0 to 2Pi value for theta

        :param quaternian_touple: takes in the (x,y,z,w) touple
        :return: a normalized theta from this function
        """
        euler_angles = tf.transformations.euler_from_quaternion(quaternian_touple)
        ## This will create a euler angle list from the quaternian information
        ## it will be in order of [Roll, Pitch, Yaw] >> Yaw is the rotation about the
        ##     ## z axis where the robot is driving in the xy plane.
        un_normalized_theta = euler_angles[2] ## This theta goes from [0,pi,-pi,0] where [0:0, pi:179 degrees, -pi:181 degrees]

        # Fixes the [0,pi,-pi,0] problem, translates to [0,2pi] over 360
        if un_normalized_theta > 0:normalized_theta = un_normalized_theta
        else: normalized_theta = (math.pi + (un_normalized_theta)) + math.pi

        return normalized_theta





