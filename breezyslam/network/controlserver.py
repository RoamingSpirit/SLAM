"""
server.py: Run in it own threads and
sends the command from the controller to the vehicle.

author: Lukas
"""

import socket
import threading

HOST = ''  # Symbolic name, meaning all available interfaces
PORT = 8000  # Arbitrary non-privileged port


class ControlServer(threading.Thread):
    # Flag for running
    running = True

    def __init__(self, vehicle):
        threading.Thread.__init__(self)
        self.socket = None
        self.connection = None
        self.connection = socket.socket()
        self.vehicle = vehicle

    def run(self):
        """
        Setup the connection and receive commands from socket.
        """
        while not self.setup() and self.running:
            pass

        self.connection.settimeout(2)
        while self.running:
            try:
                cmd = self.connection.recv(1)
                if not cmd == "":
                    if cmd == "@":
                        print "ControlServer: Emergency!"
                        self.vehicle.emergency()
                    else:
                        self.vehicle.move_manually(int(cmd))
            except socket.timeout:
                pass
            except socket.error:
                print "ControlServer: Socket error."
                self.setup()

    def setup(self):
        """
        Setup a connection to a client on port 8000.
        """
        # Bind socket to local host and port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)

        try:
            self.socket.bind((HOST, PORT))
        except socket.error:
            return False

        if self.running:
            # Start listening on socket
            self.socket.listen(2)
            print "ControlServer: Socket now listening."

            # Wait to accept a connection - blocking call
            try:
                self.connection, address = self.socket.accept()
                print "ControlServer: Socket connected with " + address[0] + ":" + str(address[1])
                return True
            except socket.error:
                return False

    def close(self):
        """
        Close the connection and stop the running thread.
        """
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)

        except socket.error:
            pass
        self.socket.close()
