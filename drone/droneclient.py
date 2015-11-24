import socket
import threading
from drone import Drone

HOST = ""
PORT = 8888

class TurtleClient(threading.Thread):

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
                self.drone = Drone()
                print "Initialize"
                self.drone.initialize()
            elif msg == "1":
                self.drone.shutdown()
                self.close()
            elif msg == "2":
                print "Move forward"
                self.drone.move(msg)
                self.socket.send(self.drone.getOdometry())
            elif msg == "3":
                print "Turn right"
                self.drone.move(msg)
                self.socket.send(self.robot.getOdometry())
            elif msg == "4":
                print "Turn left"
                self.drone.move(msg)
                self.socket.send(self.robot.getOdometry())
                
    def close(self):
        '''
        Close the connection and stop the running thread.
        '''
        self.running = False
        self.robot.shutdown()
        self.socket.close()
        print "Socket closed"

if __name__ == '__main__':
    client = TurtleClient(testBot)
    

