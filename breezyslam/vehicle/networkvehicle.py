"""
NetworkVehicle class.
"""

import socket
import time
import threading
from vehicle import Vehicle


class NetworkVehicle(Vehicle):
    """
    Class representing a connection to a robot.
    """
    HOST = ""
    PORT = 9000

    MOVE = 6
    ODOMETRY = 7
    LAND = 8
    TAKEOFF = 9
    EMERGENCY = 10

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.socket()
        self.manually_operated = True
        self.is_emergency = False
        self.odometry = [0.0, 0.0, 0.0]

    def move(self, cmd):
        """
        Send steering commands to the robot client.
        :param cmd: Move command.
        :return: Odometry data.
        """
        if not self.is_emergency:
            if not self.manually_operated:
                self.connection.send(chr(cmd))
            else:
                self.connection.send(chr(NetworkVehicle.ODOMETRY))

            # Receive and parse odometry.
            data = self.connection.recv(1024)
            values = data.split(",", 3)
            self.odometry = [float(tok) for tok in values[:]]
            return self.odometry
        return [0.0, 0.0, 0.0]

    def move_manually(self, command, values=("", "", "", "")):
        """
        Send steering commands to the robot client.
        :param command: Moving command.
        :param values: Parameters for manual moving.
        :return: None.
        """
        if not self.is_emergency:

            if command == 0:
                self.change_op_mod()
                return

            if self.manually_operated:
                self.connection.send(chr(command))
                if command == 6:
                    for i in range(0, 4):
                        self.connection.send(values[i])

    def emergency(self):
        """
        Emergency stop.
        :rtype: object
        """
        if self.is_emergency:
            self.is_emergency = False
        else:
            self.is_emergency = True

        print "NetworkVehicle: Emergency!"
        self.connection.send(chr(NetworkVehicle.EMERGENCY))

    def getOdometry(self):
        """
        Request and receive odometry.
        :return: Odometry data.
        """
        return self.move(NetworkVehicle.ODOMETRY)

    def change_op_mod(self):
        """
        Change from manually operation to auto and reverse.
        """
        if self.manually_operated:
            print "Manually op mod = False"
            self.manually_operated = False
        else:
            print "Manually op mod = True"
            self.manually_operated = True

    def initialize(self):
        """
        Initialize.
        """
        print "NetworkVehicle: Try to bind socket.."
        while not self.setup():
            pass
        self.connection.settimeout(2)
        self.connection.send(chr(0))
        msg = self.connection.recv(1)
        while chr(1) not in msg:
            msg = self.connection.recv(1)
        print "NetworkVehicle: Connected."

    def setup(self):
        """
        Setup a connection to a client on PORT.
        """
        # Bind socket to local host and port
        try:
            self.socket.bind((NetworkVehicle.HOST, NetworkVehicle.PORT))
        except socket.error:
            return False

        # Start listening on socket
        self.socket.listen(1)
        print "NetworkVehicle: Wait for client.."

        # Connect to the client
        try:
            self.connection, addr = self.socket.accept()
            print "NetworkVehicle: Connected with " + addr[0] + ":" + str(addr[1])
            return True
        except socket.error:
            self.shutdown()
            print "NetworkVehicle: Socket closed."
            return False

    def shutdown(self):
        """
        Close connection
        """
        self.connection.send(chr(1))
        self.connection.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "NetworkVehicle: Connection closed."

    # ~ if __name__ == '__main__':
    # ~ CLIENT = NetworkVehicle()
    # ~ CLIENT.initialize()
    # ~ time.sleep(10)
    # ~ CLIENT.move(MOVE_FORWARD)
    # ~ CLIENT.move(TURN_LEFT)
    # ~ CLIENT.shutdown()
