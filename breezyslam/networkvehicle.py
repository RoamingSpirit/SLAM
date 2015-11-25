import socket
from vehicle import Vehicle

HOST = ""
PORT = 9000

MOVE_FORWARD = 2
TURN_RIGHT = 3
TURN_LEFT = 4
STAGNATE = 5

class NetworkVehicle(Vehicle):

    odometry = [0.0, 0.0, 0.0]

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
        self.connection.send(chr(1))
        print chr(1)
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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            return False
            
        # Start listening on socket
        self.socket.listen(1)
        print "Wait for client.."
        
        # Connect to the client
        try:
            self.connection, addr = self.socket.accept()
            print "Connected with " + addr[0] + ":" + str(addr[1])
            return True
        except socket.error, e:
            self.close()
            print "Socket closed."
            return False

if __name__ == '__main__':
    client = NetworkVehicle()
    client.initialize()
    client.move(MOVE_FORWARD)
    client.move(TURN_LEFT)
    client.shutdown()

