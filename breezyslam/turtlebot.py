from vehicle import Vehicle
from CPI_Protocol import SCommunicator

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


class Turtlebot(Vehicle):
    def __init__(self,COMPort):
        """
        This will handle all of the initialization information for the turtlebot

        :param COMPort: String rep of the serial port to communicate on.
        :return:
        """
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

        self._com = SCommunicator.SCommunicator(COMPort)

        sleeper = rospy.Duration(1)
        rospy.sleep(sleeper)
        print "Turtlebot Initialization Complete"

    def initialize(self):
        return

    """ -----------------:::Odometry Functions ::: -----------------------"""
    def getOdometry(self):
        """

        This will run the serial commands to send the odom data. the _getOdomROS function will calculate
        and store the difference between the last time it was called and now.

        :return: Will return nothing, instead published to the serial port.
        """

    def _getOdomROS(self, msg):
        """
        This function is the ROS callback that allows the turtlebot script to know what the odometry data is for the
        turtlebot it is attached to

        :param msg: This is the message that the robot receives from listening to the '/odom' topic
        :return: None
        """
        self._past_x
        self._past_y
        self._past_theta

        self._d_theta
        self._d_traveled

        # Find the distance traveled
        self._d_traveled = math.sqrt((self._past_x - msg.pose.pose.position.x)**2 +
                               (self._past_y - msg.pose.pose.position.y)**2)

        quat = (msg.pose.pose.orientation.x,
                msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z,
                msg.pose.pose.orientation.w)

        current_theta_rad = self._normalizeTheta(quat)

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


    """ -----------------:::Drive Helpers ::: -----------------------"""
    def _driveStraight(self, speed, distance):
        """
        THis takes in a speed and distance and moves in the facing direction
        until it has reached the distance.

        NOTE: This function denotes it's travel by how far the 'odom' frame believes
        it has traveled. NOT how far it has traveled in the /map.

        :param speed: This is a 0 to 1 value, it will cap the values at 1 and 0.
        :param distance: This is a value in meters.
        :return: Nothing
        """

        ## Speed Error checking
        def distFormula(point1, point2):
            """
            :param point1: Touple in the form of (x1, y1)
            :param point2: Touple in the form of (x2, y2)
            :return: Returns Distance between two points
            """
            # print "DistForm: ",point1, point2

            x1, y1 = point1
            x2, y2 = point2

            return math.sqrt((x1-x2)**2 + (y1-y2)**2)

        if speed > 1: speed = 1
        elif speed < 0: speed = 0

        ## Set the starting x,y
        starting_x = self._x
        starting_y = self._y

        ## Booleans for understanding location
        arrived = False
        slowdown = False

        while ((not arrived) and (not rospy.is_shutdown())):
            ## Get the distance traveled
            dist_so_far = distFormula((starting_x,starting_y),(self._x,self._y))

            ## Modulate speed based off how far you've gone
            if dist_so_far <= abs(distance)*0.25:
                print 'there'
                regulated_speed = speed*(0.2) + speed*(dist_so_far / distance)
            elif dist_so_far >= abs(distance)*0.75:
                print 'Here'
                regulated_speed = speed*(0.2) + speed*(1- (dist_so_far / distance))
            else:
                regulated_speed = speed
            if distance > 0: self._spinWheels(regulated_speed,regulated_speed,0.1)
            else: self._spinWheels(-regulated_speed,-regulated_speed,0.1)

            #Set the booleans on if you're there yet
            arrived = dist_so_far >= abs(distance)

        self._stopRobot()

    def rotate(self, angle, speed = 0.05):
        """
        :param angle: <int or double> the angle the robot should turn in degrees
        :param speed: <int or double> The speed at which the robot should rotate
        :return: None
        """
        ## Error Checking Angle:
        if angle == 0: return
        else: done = False

        angle_to_travel_rad = math.radians(angle)
        start_theta_rad = self._normalizeTheta(self._quat)
        print angle_to_travel_rad, start_theta_rad
        # print ("angle to travel", "start theta", "Current theta", "d_theta")

        while not done and (not rospy.is_shutdown()):
            current_theta_rad = self._normalizeTheta(self._quat)

            # Calculates the difference in the thetas
            # This keeps track of
            debug_state = None
            if start_theta_rad > current_theta_rad and start_theta_rad > math.pi*3/2 and current_theta_rad < math.pi/2:
                d_theta = ((2*math.pi) - start_theta_rad) + current_theta_rad
                debug_state = 1
            elif start_theta_rad < current_theta_rad and start_theta_rad < math.pi/2 and current_theta_rad > math.pi*3/2:
                d_theta = ((2*math.pi) - current_theta_rad) + start_theta_rad
                debug_state = 2
            else:
                d_theta = start_theta_rad - current_theta_rad
                debug_state = 3

            print angle_to_travel_rad, start_theta_rad, current_theta_rad, d_theta, debug_state
            ## If you're within 0.1 Radian stop
            if abs(angle_to_travel_rad) - abs(d_theta) < 0.1:
                done = True
                self._stopRobot()
            else:
                if (angle > 0):
                    self._spinWheels(speed,-speed,.1)
                else:
                    self._spinWheels(-speed,speed,.1)


    def _stopRobot(self):
        """  Publishes a stop message to the robot
        :return:None
        """
        self._publishTwist(0,0)

    def _spinWheels(self,u1,u2,timesec):
        """
        This will spin the left wheel u1 and the right wheel u2 for timesec <seconds>

        :param u1: left Wheel velocity
        :param u2: Right Wheel Velocity
        :param timesec: How long this will happen for
        :return: None
        """
        lin_vel = (0.5)*(u1 + u2)
        ang_vel = (1/(self._wheelbase))*(u1-u2)

        start = time.time()
        while ((time.time() - start) < timesec and (not rospy.is_shutdown())):
            self._publishTwist(lin_vel, ang_vel)
        ## stop Robot
        self._stopRobot()
        return

    def _publishTwist(self, u, w):
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

        self._pub.publish(twist)

