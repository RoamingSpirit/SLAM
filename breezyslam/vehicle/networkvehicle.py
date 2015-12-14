"""
NetworkVehicle class.
"""
import socket
from vehicle import Vehicle

__author__ = "Lukas"


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

    def __init__(self, log=True):
        self.log = log
        if log:
            self.out = open('odomerty', 'w')

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.socket()
        self.manually_operated = False
        self.is_emergency = False
        self.size = 0.0
        self.odometry = [0.0, 0.0, 0.0]

    def move(self, cmd):
        """
        Send steering commands to the robot client.
        :param cmd: Move command.
        :return: Odometry data.
        """
        try:
            if not self.is_emergency:
                if not self.manually_operated:
                    self.connection.send(chr(cmd))
                else:
                    self.connection.send(chr(NetworkVehicle.ODOMETRY))

                # Receive and parse odometry.
                data = self.connection.recv(1024)
                values = data.split(",", 3)
                self.odometry = [float(tok) for tok in values[:]]
                if self.log:
                    self.out.write("%f %f %f\n" % (self.odometry[0], self.odometry[1], self.odometry[2]))
                return self.odometry
        except socket.timeout:
            print "NetworkVehicle: Timeout: Return [0.0, 0.0, 0.0]."
        except ValueError:
            print "NetworkVehicle: ValueError: Return [0.0, 0.0, 0.0]."
        except socket.error, error:
            print "NetworkVehicle: ", error, "Return None."
            return None
        return [0.0, 0.0, 0.0]

    def move_manually(self, command, values=("", "", "", "")):
        """
        Send steering commands to the robot client.
        :param command: Moving command.
        :param values: Parameters for manual moving.
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

    def getSize(self):
        """
        Return the size of the vehicle.
        :return: Size.
        """
        return self.size

    def initialize(self):
        """
        Initialize.
        """
        print "NetworkVehicle: Try to bind socket.."
        while not self.setup():
            pass
        try:
            self.connection.settimeout(2)
            self.connection.send(chr(0))
            msg = self.connection.recv(1)
            while "\n" not in msg:
                msg += self.connection.recv(1)
            msg = msg.split("\n")
            self.size = float(msg[0])

            print "NetworkVehicle: Connected."
        except socket.timeout:
            print "Timeout."
        except socket.error, error:
            print error

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
            self.connection, address = self.socket.accept()
            print "NetworkVehicle: Connected with " + address[0] + ":" + str(address[1])
            return True
        except socket.error:
            self.shutdown()
            print "NetworkVehicle: Socket closed."
            return False

    def shutdown(self):
        """
        Close connection.
        """
        if self.log:
            self.out.close()
        try:
            self.connection.send(chr(1))
            self.connection.close()
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            print "NetworkVehicle: Connection closed."
        except socket.timeout:
            print "Timeout."
        except socket.error, error:
            print error

            # ~ if __name__ == '__main__':
            # ~ CLIENT = NetworkVehicle()
            # ~ CLIENT.initialize()
            # ~ time.sleep(10)
            # ~ CLIENT.move(MOVE_FORWARD)
            # ~ CLIENT.move(TURN_LEFT)
            # ~ CLIENT.shutdown()
