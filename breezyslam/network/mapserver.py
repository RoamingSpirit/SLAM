"""
server.py:
"""

import socket
import threading

HOST = ''  # Symbolic name, meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port


class MapServer(threading.Thread):
    # Flag for running
    running = True

    def __init__(self, slam, MAP_SIZE_PIXELS):
        threading.Thread.__init__(self)
        self.socket = None
        self.connection = None
        self.slam = slam
        self.MAP_SIZE_PIXELS = MAP_SIZE_PIXELS

    def run(self):

        """
        Opens a second and waits till a client connects.
        Then sends the map updates till the client disconnects.
        Start over.
        """
        while not self.setup() and self.running:
            pass

        while self.running:
            # Create a byte array to receive the computed maps
            mapb = bytearray(self.MAP_SIZE_PIXELS * self.MAP_SIZE_PIXELS)

            # Get final map    
            self.slam.getmap(mapb)
            try:
                self.connection.send(mapb)
            except socket.error:
                print "MapServer: Client disconnected"
                if self.running:
                    self.setup()

    def setup(self):
        """
        Setup a connection to a client on port 8000.
        """
        # Bind socket to local host and port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.bind((HOST, PORT))
        except socket.error:
            return False

        if self.running:
            # Start listening on socket
            self.socket.listen(2)
            print "MapServer: Socket now listening."

            # Wait to accept a connection - blocking call
            try:
                self.connection, address = self.socket.accept()
                print "MapServer: Socket connected with " + address[0] + ":" + str(address[1])
                self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
                return True
            except socket.error:
                return False

    def close(self):
        """
        Close the server.
        """
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
            
        except socket.error:
            pass
        self.socket.close()
            
