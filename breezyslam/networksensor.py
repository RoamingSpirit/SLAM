import socket
from vehicle import Vehicle

HOST = ""
PORT = 9001

class NetworkSensor():

    def get_frame(self):
        '''
        Request a new frame.
        '''
        self.connection.send("2")
        msg = ""
        #~ while "\n" not in msg:
            #~ msg += self.connection.recv(1024)
        #~ frame = msg.split("\n")
        #~ return frame[0]

    def initialize(self):
        '''
        Iinitialize
        '''          
        self.setup()
        self.connection.send("0")
        print "Connected."
            
    def shutdown(self):
        '''
        Close connection
        '''
        self.connection.send("1")
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
            print "Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
        # Start listening on socket
        self.socket.listen(1)
        
        # Connect to the client
        try:
            self.connection, addr = self.socket.accept()
            print "Connected with " + addr[0] + ":" + str(addr[1])
        except socket.error, e:
            self.close()
            print "Socket closed"

#~ if __name__ == '__main__':
    #~ client = NetworkSensor()
    #~ client.initialize()
    #~ client.get_frame()
    #~ client.shutdown()

