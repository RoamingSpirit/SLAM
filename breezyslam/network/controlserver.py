'''
server.py: Run in it own threads and
sends the command from the gamepad to the vehicle.

author: Lukas
'''
 
import socket
import threading
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8000 # Arbitrary non-privileged port

class ControlServer(threading.Thread):
    #Flag for running
    running = True
    
    def __init__(self, vehicle):
        threading.Thread.__init__(self)
        self.vehicle = vehicle

    '''
    Setup the connection and receive commands from socket.
    '''
    def run(self):

        while not self.setup():
            pass
        
        while(self.running):
            try:
                cmd = self.connection.recv(1)
                if not cmd == "":
                    if cmd == "@":
                        print "ControlServer: Emergency!"
                        self.vehicle.emergency()
                    elif cmd == "6":
                        x = self.connection.recv(1)
                        y = self.connection.recv(1)
                        z = self.connection.recv(1)
                        rz = self.connection.recv(1)
                        print "Commands: ", ord(x), ord(y), ord(z), ord(rz)
                        self.vehicle.move_manually(int(cmd), (x, y, z, rz))
                    else:
                        self.vehicle.move_manually(int(cmd))
            except socket.error, e:
                print "ControlServer: Client disconnected."
                self.setup()

    '''
    Setup a connection to a client on port 8000.
    '''
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         
        # Bind socket to local host and port
        try:
            self.socket.bind((HOST, PORT))
        except socket.error as msg:
            return False
            
        if(self.running):             
            # Start listening on socket
            self.socket.listen(2)
            print 'ControlServer: Socket now listening.'
            
            # Wait to accept a connection - blocking call
            try:
                self.connection, addr = self.socket.accept()
                print 'ControlServer: Socket connected with ' + addr[0] + ':' + str(addr[1])
                return True
            except socket.error, e:
                print 'ControlServer: Socket closed.'
                return False

    '''
    Close the connection and stop the running thread.
    '''
    def close(self):
        self.running = False
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()      
