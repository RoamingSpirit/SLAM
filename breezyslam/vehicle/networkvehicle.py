'''
NetworkVehilce class.
'''

import socket, time, threading
from vehicle import Vehicle

class NetworkVehicle(Vehicle):
    '''
    Class representing a connection to a robot.
    '''
    HOST = ""
    PORT = 9000

    MOVE = 6
    STAGNATE = 7
    LAND = 8
    TAKEOFF = 9
    EMERGENCY = 10

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.manually_operated = False
        self.odometry = [0.0, 0.0, 0.0]
        self.lock = threading.RLock()

    def move(self, cmd):
        '''
        Send steering commands to the robot client.
        '''
        self.lock.acquire()
        if not self.manually_operated:
            self.connection.send(chr(cmd))
        else:
            self.connection.send(chr(STAGNATE))
            
        data = self.connection.recv(1024)
        self.lock.release()
        toks = data.split(",", 3)
        self.odometry = [float(tok) for tok in toks[:]]
        return self.odometry
        
    def move_manually(self, cmd):
        '''
        Send steering commands to the robot client.
        '''
        string = cmd.split(".", 2)
            
        if self.manually_operated:
            self.lock.acquire()
            self.connection.send(chr(string[0]))
            if string[0] == "6":
                self.connection.send(string[1])
            data = self.connection.recv(1024)
            self.lock.release()
    
    def emergency(self):
        '''
        Emergency stop.
        '''
        self.connection.send(chr(EMERGENCY))

    def getOdometry(self):
        '''
        Request and receive odometry.
        '''
        return self.move(STAGNATE)
        
    def change_op_mod(self):
        '''
        Change from manually operation to auto and reverse.
        '''
        if self.manually_operated:
            self.manually_operated = False
        else:
            self.manually_operated = True
            self.move(HOVER)

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

    def shutdown(self):
        '''
        Close connection
        '''
        self.connection.send(chr(1))
        self.connection.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "Connection closed."

#~ if __name__ == '__main__':
    #~ CLIENT = NetworkVehicle()
    #~ CLIENT.initialize()
    #~ time.sleep(10)
    #~ CLIENT.move(MOVE_FORWARD)
    #~ CLIENT.move(TURN_LEFT)
    #~ CLIENT.shutdown()

