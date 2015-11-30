'''
NetworkVehilce class.
'''

import socket, time
from vehicle import Vehicle

HOST = ""
PORT = 9000

MOVE_FORWARD = 2
TURN_RIGHT = 3
TURN_LEFT = 4
STAGNATE = 5

class NetworkVehicle(Vehicle):
    '''
    Class representing a connection to a robot.
    '''
    odometry = [0.0, 0.0, 0.0]

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def move(self, cmd):
        '''
        Send steering commands to the robot client.
        '''
        self.connection.send(chr(cmd))
        data = self.connection.recv(1024)
        toks = data.split(",", 3)
        self.odometry = [float(tok) for tok in toks[:]]
        return self.odometry

    def getOdometry(self):
        '''
        Request and receive odometry
        '''
        return self.move(STAGNATE)

    def initialize(self):
        '''
        Iinitialize
        '''
        print "Try to bind socket.."
        while not self.setup():
            pass
        self.connection.send(chr(0))
        msg = self.connection.recv(1)
        while chr(1) not in msg:
            msg = self.connection.recv(1)
        print "Connected."

    def shutdown(self):
        '''
        Close connection
        '''
        self.connection.send(chr(1))
        self.connection.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "Connection closed."

    def setup(self):
        '''
        Setup a connection to a client on PORT.
        '''
        # Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error:
            return False

        # Start listening on socket
        self.socket.listen(1)
        print "Wait for client.."

        # Connect to the client
        try:
            self.connection, addr = self.socket.accept()
            print "Connected with " + addr[0] + ":" + str(addr[1])
            return True
        except socket.error:
            self.shutdown()
            print "Socket closed."
            return False

#~ if __name__ == '__main__':
    #~ CLIENT = NetworkVehicle()
    #~ CLIENT.initialize()
    #~ time.sleep(10)
    #~ CLIENT.move(MOVE_FORWARD)
    #~ CLIENT.move(TURN_LEFT)
    #~ CLIENT.shutdown()

