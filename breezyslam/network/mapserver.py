'''
server.py: Runs in it own threads and sends the map to a connected clients in a loop

author: Nils Bernhardt
'''
 
import socket
import threading
from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

class MapServer(threading.Thread):
    #flag for running
    running = True
    
    def __init__(self, slam, MAP_SIZE_PIXELS):
        threading.Thread.__init__(self)
        self.slam = slam
        self.MAP_SIZE_PIXELS = MAP_SIZE_PIXELS
        
    '''
    Opens a second and waits till a client connects.
    Then sends the map updates till the client disconnects.
    Start over.
    '''
    def run(self):

        self.setup()
        
        while(self.running):
            # Create a byte array to receive the computed maps
            mapb = bytearray(self.MAP_SIZE_PIXELS * self.MAP_SIZE_PIXELS)

            # Get final map    
            self.slam.getmap(mapb)
            try:
                self.connection.send(mapb)
            except socket.error, e:
                print "Client disconnected"
                self.setup()

    '''
    Setups a connection to a client on port 8888.
    '''
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Map socket created'
         
        #Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            self.running = False
            
        if(self.running):
            #Start listening on socket
            self.socket.listen(1)
            print 'Map socket now listening'
             
            #now keep talking with the client
            #wait to accept a connection - blocking call
            try:
                self.connection, addr = self.socket.accept()
                print 'Map socket connected with ' + addr[0] + ':' + str(addr[1])
                self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
            except socket.error, e:
                self.running = False
                print 'socket closed'

    '''
    closes the connection and stops the running thread.
    '''
    def close(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()      
