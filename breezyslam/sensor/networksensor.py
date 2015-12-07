"""
networksensor.py: Representing a TCP connection to a sensor.

author: Lukas Brauckmann
"""
import socket
from sensor import Sensor

HOST = ""
PORT = 9001


class NetworkSensor(Sensor):

    def __init__(self, width, scan_rate_hz, viewangle, distance_no_detection_mm, detectionMargin, offsetMillimeters):
        super.__init__(self, width, scan_rate_hz, viewangle, distance_no_detection_mm, detectionMargin, offsetMillimeters)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = socket.socket()

    def get_frame(self):
        """
        Request a new frame.
        :return: Frame data.
        """
        self.connection.send(chr(2))
        scan = ""
        while "\n" not in scan:
            scan += self.connection.recv(1)

        values = data.split(",", 3)
        frame = [float(tok) for tok in values[:]]

        return frame

    def initialize(self):
        """
        Initialize.
        """
        while not self.setup():
            pass
        self.connection.send("0")
        print "Connected."

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
