import socket
import threading
from vehicle import Vehicle
#from turtlebot import Turtlebot

HOST = ""
PORT = 9999

class SensorClient(threading.Thread):

    running = True

    def __init__(self, host = ""):
        threading.Thread.__init__(self)
        HOST = host
        self.start()

    def run(self):
        '''
        Main loop
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        
        while self.running:
            msg = self.socket.recv(1)
            if msg == "":
                pass
            else:
                print msg
            if msg == "0":
                print "Initialize"
            elif msg == "1":
                self.close()
            elif msg == "2":
                #TODO: get_frame()
                print "Request frame"
                
    def close(self):
        '''
        Close the connection and stop the running thread.
        '''
        self.running = False
        self.socket.close()
        print "Socket closed"

if __name__ == '__main__':
    client = SensorClient()
        

