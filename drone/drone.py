'''
Drone class.
'''

__author__ = "lukas"
__date__ = "$10.11.2015 10:12:49$"

# ~ import sys
# ~ sys.path.insert(0, '/home/pi/libardrone/python-ardrone')
import sys

sys.path.insert(0, '/home/lukas/Dokumente/Libs/libardrone/python-ardrone')
from vehicle import Vehicle
import libardrone
import cv2
import time
import math

DRONE_SPEED = 0.1
TESTING = True


class Drone(Vehicle):
    """
    Class representing a connection to the ARDrone,
    controls it and receive navdata information.
    """

    correct_psi = True
    in_air = False
    cmd = 0
    commands = [0.0, 0.0, 0.0, 0.0]
    old_timestamp = 0.0

    def __init__(self, log=True):
        """
        Initialize the connection and variables.
        """
        self.log = log
        if log:
            self.out = open('odometry', 'w')
        print "Drone: Establish connection to the drone..."
        self.cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        self.drone = libardrone.ARDrone()
        print "Drone: Ok."
        self.last_thata = self.drone.navdata.get(0, dict()).get('psi', 0)
        self.size = 0.3

    def get_dt(self):
        """
        Return the time difference since the last update.
        """
        now = time.time()
        if self.old_timestamp == 0.0:
            self.old_timestamp = now
            return 0.0
        dt_seconds = now - self.old_timestamp
        self.old_timestamp = now
        return dt_seconds

    @classmethod
    def calc_distance(cls, velocity_x, dt_seconds):
        """
        Calculate distance since last frame.
        :param dt_seconds: Time since last call.
        :param velocity_x: Current velocity
        """
        return velocity_x * dt_seconds

    def calc_dthata(self, thata):
        """
        Calculate dthata since last call.
        :param thata: Current rotate angle.
        """
        dthata = thata - self.last_thata
        if dthata > 180:
            dthata -= 360
        elif dthata < -180:
            dthata += 360
        self.last_thata = thata
        return dthata

    def get_odometry(self):
        """
        Return a tuple of odometry (dxy in mm,dthata in degree, dt in s) and
        send move commands to the drone.
        """
        # Move the drone
        if self.in_air and (not TESTING):
            if self.cmd == 2:
                print "Move forward"
                self.drone.move(0, -DRONE_SPEED, 0, 0)
            elif self.cmd == 3:
                print "Turn right"
                self.drone.move(0, 0, 0, DRONE_SPEED)
            elif self.cmd == 4:
                print "Turn left"
                self.drone.move(0, 0, 0, -DRONE_SPEED)
            elif self.cmd == 5:
                print "Hover"
                self.drone.hover()
            elif self.cmd == 6:
                print "Move command:"
                print self.commands[0], self.commands[1], self.commands[2], self.commands[3]
                self.drone.move(self.commands[0], self.commands[1], self.commands[2], self.commands[3])
            elif self.cmd == 8:
                self.drone.land()
            elif self.cmd == 9:
                self.drone.takeoff()

        # Get odometry data
        dt_seconds = self.get_dt()
        dthata = self.calc_dthata(self.drone.navdata.get(0, dict())
                                  .get('psi', 0))
        if self.correct_psi & (math.fabs(dthata) > 20):
            dthata = 0
            self.correct_psi = False

        dx_mm = Drone.calc_distance(self.drone.navdata.get(0, dict())
                                    .get('vx', 0), dt_seconds)
        dy_mm = self.calc_distance(self.drone.navdata.get(0, dict())
                                   .get('vy', 0), dt_seconds)
        dxy = math.sqrt(dx_mm * dx_mm + dy_mm * dy_mm)

        data = dxy, dthata, dt_seconds

        if self.log:
            self.out.write("%f %f %f\n" % data)

        return "%f,%f,%f" % data

    def move(self, cmd):
        """
        Set the moving command.
        :param cmd:  Command.
        """
        self.cmd = cmd

    def manually_move(self, x, y, z, rz):
        """
        Set the moving command.
        """
        self.cmd = 6
        self.commands[0] = x
        self.commands[1] = y
        self.commands[2] = -z
        self.commands[3] = rz
        print "Commands: ", self.commands

    def land(self):
        """
        Land.
        """
        self.drone.land()
        self.in_air = False

    def emergency(self):
        """
        Emergency landing.
        """
        self.drone.reset()
        self.in_air = False

    def getSize(self):
        return self.size

    def initialize(self):
        """
        Let the drone fly.
        """
        print "Drone: Take off"
        if not TESTING and self.in_air:
            self.drone.takeoff()
            self.drone.hover()
            counter = 0
            # Check if the drone is in air and hovering
            # ~ while self.in_air == False:
            # ~ if (self.drone.navdata.get(0, dict()).
            # ~ get('state', 0) == 4) or (counter == 10):
            # ~ self.in_air = True
            # ~ counter += 1
            # ~ time.sleep(1)
            # TODO: Testing
        self.in_air = True
        print "Drone: In air!"

    def shutdown(self):
        """
        Close application.
        """
        print "Drone: Shutting down..."
        self.in_air = False
        self.drone.land()
        self.cam.release()
        self.drone.halt()
        print "Drone: Shut down."
