"""
server.py: Create a MapServer and a ControlServer.

author: Lukas
"""

from mapserver import MapServer
from controlserver import ControlServer


class Server(object):
    def __init__(self, slam, MAP_SIZE_PIXELS, vehicle):
        self.map_server = MapServer(slam, MAP_SIZE_PIXELS)
        self.control_server = ControlServer(vehicle)

    def start(self):
        """
        Start the server.
        """
        self.map_server.start()
        self.control_server.start()

    def close(self):
        """
        Close the server.
        """
        self.map_server.close()
        self.map_server.join()
        print "MapServer closed."

        self.control_server.close()
        self.control_server.join()
        print "ControlServer closed."
