# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Lukas"
__date__ = "$03.11.2015 15:41:03$"

import socket

class SimpleReceiver:
    
    """
    Class representing a socket that is listening on 'localhost' and receiving data.
    """
    def __init__(self):
        """Initialize the class variables"""
        self.BUFFER_SIZE = 1024
        self.SERVER_ADDRESS = ('localhost', 3490)

    def connect(self):
         """Connect to host"""
         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.s.connect(self.SERVER_ADDRESS)
         print "Connected to: ", self.SERVER_ADDRESS

    def listen(self):
        while 1:
            """Listen and receive data"""
            data = self.s.recv(self.BUFFER_SIZE)
            print data
        self.s.close()
        print "Closed socket"

    #msg = "Success!"
    #s.send(msg)
