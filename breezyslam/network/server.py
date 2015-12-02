'''
server.py: Create a MapServer and a ControlServer.

author: Lukas
'''

from mapserver import MapServer
from controlserver import ControlServer

class Server():
    
    def __init__(self, slam, MAP_SIZE_PIXELS, vehicle):
        self.map_server = MapServer(slam, MAP_SIZE_PIXELS)
        self.control_server = ControlServer(vehicle)

    '''
    Start server.
    '''
    def start(self):
        self.map_server.start()
        self.control_server.start()

    '''
    Close the server.
    '''
    def close(self):
        self.map_server.close()
        self.control_server.close()      
