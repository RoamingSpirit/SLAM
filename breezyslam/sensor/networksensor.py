"""
networksensor.py: Representing a TCP connection to a sensor.

author: Lukas Brauckmann
"""
import socket
from sensor import Sensor

HOST = ""
PORT = 9001


class NetworkSensor(Sensor):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.socket()

        self.width = 0
        self.scan_rate_hz = 0
        self.viewangle = 0
        self.distance_no_detection_mm = 0
        self.detection_margin = 0
        self.offset_millimeters = 0

        self.initialize()

        Sensor.__init__(self, self.width, self.scan_rate_hz, self.viewangle,
                       self.distance_no_detection_mm, self.detection_margin, self.offset_millimeters)

    def scan(self):
        """
        Request a new frame.
        :return: Frame data.
        """
        self.connection.send(chr(2))
        scan = ""
        while "\n" not in scan:
            scan += self.connection.recv(1)

        values = scan.split(",")
        frame = [int(tok) for tok in values[:]]
        return frame

    def initialize(self):
        """
        Initialize.
        """
        while not self.setup():
            pass
        print "Connected."
        self.connection.send(chr(0))
        scan = ""
        while "\n" not in scan:
            scan += self.connection.recv(1)
        values = scan.split(",",5)
        print len(values)
        for value in values:
            print value
        parameters = [int(tok) for tok in values[:]]
        self.width = parameters[0]
        self.scan_rate_hz = parameters[1]
        self.viewangle = parameters[2]
        self.distance_no_detection_mm = parameters[3]
        self.detection_margin = parameters[4]
        self.offset_millimeters = parameters[5]
        print "Initialized."

    def setup(self):
        """
        Setup a connection to a client on PORT.
        :return: Successful connected to host.
        """
        # Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            return False

        # Start listening on socket
        self.socket.listen(1)

        # Connect to the client
        try:
            self.connection, address = self.socket.accept()
            print "Connected with " + address[0] + ":" + str(address[1])
            return True
        except socket.error:
            self.close()
            print "Socket closed."
            return False

    def shutdown(self):
        """
        Close connection.
        """
        self.connection.send("1")
        self.connection.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "Connection closed."

        # ~ if __name__ == '__main__':
        # ~ client = NetworkSensor()
        # ~ client.initialize()
        # ~ client.get_frame()
        # ~ client.shutdown()
