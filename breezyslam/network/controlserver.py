'''
server.py: Runs in it own threads and sends the map to a connected clients in a loop

author: Lukas
'''
 
import socket
import threading
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8889 # Arbitrary non-privileged port

class ControlServer(threading.Thread):
    #Flag for running
    running = True
    
    def __init__(self, vehicle):
        threading.Thread.__init__(self)
        self.vehicle = vehicle

    '''
    Opens a second and waits till a client connects.
    Then sends the map updates till the client disconnects.
    Start over.
    '''
    def run(self):

        self.setup()
        
        while(self.running):
            try:
                cmd = self.connection.recv(1024)
                if cmd == "10":
                    vehicle.emergency()
                else:
                    vehicle.move(cmd)
            except socket.error, e:
                print "Client disconnected"
                self.setup()

    '''
    Setups a connection to a client on port 8888.
    '''
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Control socket created'
         
        #Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            self.running = False
            
        if(self.running):             
            #Start listening on socket
            self.socket.listen(2)
            print 'Control socket now listening'
             
            #now keep talking with the client
            #wait to accept a connection - blocking call
            try:
                self.connection, addr = self.socket.accept()
                print 'Control socket connected with ' + addr[0] + ':' + str(addr[1])
                self.connection.sendall(str(self.MAP_SIZE_PIXELS)+"\n")
            except socket.error, e:
                self.running = False
                print 'Socket closed'

    '''
    closes the connection and stops the running thread.
    '''
    def close(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()      
