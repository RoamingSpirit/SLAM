__author__ = 'Troy Hughes'
#!/usr/bin/env python

#Author: Troy Hughes
#3002 Communication Code

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

def normalizeTheta(quaternian_touple):
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



def getOdom(msg):
    global past_x
    global past_y
    global past_theta

    global d_theta
    global d_traveled

    # Find the distance traveled
    d_traveled = math.sqrt((past_x - msg.pose.pose.position.x)**2 +
                           (past_y - msg.pose.pose.position.y)**2)

    quat = (msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w)

    current_theta_rad = normalizeTheta(quat)

    # Calculates the difference in the thetas
    if past_theta > current_theta_rad and past_theta > math.pi*3/2 and current_theta_rad < math.pi/2:
        d_theta = ((2*math.pi) - past_theta) + current_theta_rad
    elif past_theta < current_theta_rad and past_theta < math.pi/2 and current_theta_rad > math.pi*3/2:
        d_theta = ((2*math.pi) - current_theta_rad) + past_theta
    else:
        d_theta = past_theta - current_theta_rad



    # Store for next calculation
    past_x = msg.pose.pose.position.x
    past_y = msg.pose.pose.position.y
    past_theta = current_theta_rad




def main():
    global sub
    global odom_tf
    global past_x
    global past_y
    global past_theta

    rospy.init_node('Roaming_Spirit_Get_Odom')
    sub = rospy.Subscriber('/odom', Odometry, getOdom, queue_size=3)
    

    odom_list = tf.TransformListener()

    odom_tf = tf.TransformBroadcaster()
    past_x = 0; past_y = 0; past_theta = 0;
    odom_tf.sendTransform((0, 0, 0),(0, 0, 0, 1),rospy.Time.now(),"base_footprint","odom")

    ## Sleep for setup
    sleeper = rospy.Duration(1)
    rospy.sleep(sleeper)

    ser = serial.Serial(
        port = '/dev/ttyACM0',
        baudrate=115200
    )

    ser.open()


    try:
        while not rospy.is_shutdown():
            #print (past_x, past_y, past_theta)
            rospy.sleep(0.1)

            continue
    except KeyboardInterrupt:
        ser.close()
        return

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
