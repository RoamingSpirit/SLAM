'''
server.py: Runs in it own threads and sends the map to a connected clients in a loop

author: Nils Bernhardt
'''
 
import socket
import sys
import threading
from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM
from time import time
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

class Server(threading.Thread):
    #flag for running
    running = True
    
    def __init__(self, slam, MAP_SIZE_PIXELS):
        threading.Thread.__init__(self)
        self.slam = slam
        self.MAP_SIZE_PIXELS = MAP_SIZE_PIXELS

    '''
    opens a second and waits till a client connects.
    Then sends the map updates till the client disconnects.
    Start over.
    '''
    def run(self):

        self.setup()
        self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
        
        while(self.running):
            if(self.valid):
                # Create a byte array to receive the computed maps
                mapb = bytearray(self.MAP_SIZE_PIXELS * self.MAP_SIZE_PIXELS)

                # Get final map    
                self.slam.getmap(mapb)
                try:
                    self.connection.send(mapb)
                except socket.error, e:
                    print "Client disconnected"
                    self.setup()
                    self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
            else:
                self.running = False

    '''
    Setups a connection to a client on port 8888.
    '''
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
         
        #Bind socket to local host and port
        self.valid = True
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            self.valid = False
        if(self.valid):     
            print 'Socket bind complete'
             
            #Start listening on socket
            self.socket.listen(10)
            print 'Socket now listening'
             
            #now keep talking with the client
            #wait to accept a connection - blocking call
            
            self.connection, addr = self.socket.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            

    '''
    closes the connection and stops the running thread.
    '''    def close(self):
        self.running = False
        if(self.valid):
            self.socket.close()
