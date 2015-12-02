'''
server.py: 
'''

import socket
import threading

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
        
        while(self.running):
            # Create a byte array to receive the computed maps
            mapb = bytearray(self.MAP_SIZE_PIXELS * self.MAP_SIZE_PIXELS)

            # Get final map    
            self.slam.getmap(mapb)
            try:
                self.connection.send(mapb)
            except socket.error, e:
                print "Client disconnected"
                if(self.running):
                    self.setup()


    '''
    Start server..
    '''
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
         
        #Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            self.running = False
            
        if(self.running):     
            print 'Socket bind complete'
             
            #Start listening on socket
            self.socket.listen(0)
            print 'Socket now listening'
             
            #now keep talking with the client
            #wait to accept a connection - blocking call
            try:
                self.connection, addr = self.socket.accept()
                print 'Connected with ' + addr[0] + ':' + str(addr[1])
                self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
            except socket.error, e:
                self.running = False
                print 'socket closed'
            
            


    '''
    Close the server.
    '''
    def close(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
