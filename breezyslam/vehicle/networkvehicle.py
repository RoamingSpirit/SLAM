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
    ODOMETRY = 7
    LAND = 8
    TAKEOFF = 9
    EMERGENCY = 10

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.manually_operated = False
        self.odometry = [0.0, 0.0, 0.0]
        self.lock = threading.Lock()

    def move(self, cmd):
        '''
        Send steering commands to the robot client.
        '''
        self.lock.acquire()
        if not self.manually_operated:
            print "Move."
            self.connection.send(chr(cmd))
        else:
            print "Just receive odometry."
            self.connection.send(chr(NetworkVehicle.ODOMETRY))
            
        data = self.connection.recv(1024)
        self.lock.release()
        toks = data.split(",", 3)
        self.odometry = [float(tok) for tok in toks[:]]
        return self.odometry

    def move_manually(self, cmd):
        '''
        Send steering commands to the robot client.
        '''
        string = cmd.split(";", 2)
        command = int(string[0])
        if not command == 6:
            print command
        
        if command == 0:
            self.change_op_mod()
            return
            
        if self.manually_operated:
            self.lock.acquire()
            print "Move manually."
            self.connection.send(chr(command))
            if command == 6:
                self.connection.send(string[1])
            self.lock.release()

    def emergency(self):
        '''
        Emergency stop.
        '''
        self.lock.acquire()
        self.connection.send(chr(NetworkVehicle.EMERGENCY))
        self.lock.release()

    def getOdometry(self):
        '''
        Request and receive odometry.
        '''
        return self.move(NetworkVehicle.ODOMETRY)
        
    def change_op_mod(self):
        '''
        Change from manually operation to auto and reverse.
        '''
        if self.manually_operated:
            print "Manually op mod = False"
            self.manually_operated = False
        else:
            print "Manually op mod = True"
            self.manually_operated = True

    def initialize(self):
        '''
        Iinitialize
        '''
        print "NetworkVehicle: Try to bind socket.."
        while not self.setup():
            pass
        self.connection.send(chr(0))
        msg = self.connection.recv(1)
        while chr(1) not in msg:
            msg = self.connection.recv(1)
        print "NetworkVehicle: Connected."
        
    def setup(self):
        '''
        Setup a connection to a client on PORT.
        '''
        # Bind socket to local host and port
        try:
            self.socket.bind((NetworkVehicle.HOST, NetworkVehicle.PORT))
        except socket.error:
            return False

        # Start listening on socket
        self.socket.listen(1)
        print "NetworkVehicle: Wait for client.."

        # Connect to the client
        try:
            self.connection, addr = self.socket.accept()
            print "NetworkVehicle: Connected with " + addr[0] + ":" + str(addr[1])
            return True
        except socket.error:
            self.shutdown()
            print "NetworkVehicle: Socket closed."
            return False

    def shutdown(self):
        '''
        Close connection
        '''
        self.connection.send(chr(1))
        self.connection.close()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "NetworkVehicle: Connection closed."

#~ if __name__ == '__main__':
    #~ CLIENT = NetworkVehicle()
    #~ CLIENT.initialize()
    #~ time.sleep(10)
    #~ CLIENT.move(MOVE_FORWARD)
    #~ CLIENT.move(TURN_LEFT)
    #~ CLIENT.shutdown()

