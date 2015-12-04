'''
TurtleClient class.
'''

import socket
import threading

class TurtleClient(threading.Thread):
    '''
    Class representing a client which receive drone commands
    and send drone odometry.
    '''
    running = True

    def __init__(self, host = "", port = 9000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.turtle = TurtleBot()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.start()

    def run(self):
        '''
        Main loop
        '''
        print "TurtleClient: Connecting.."
        self.socket.connect((self.host, self.port))
        print "TurtleClient: Connected to host."

        while self.running:
            try:
                msg = self.socket.recv(1)
                if len(msg) == 0:
                    print "Connection to server lost."
                    self.close()
                elif msg == chr(10):
                    print "Emergency."
                    self.turtle.emergency()
                elif msg == chr(0):
                    print "Initialize."
                    self.turtle.initialize()
                    self.socket.send(chr(1))
                elif msg == chr(1):
                    print "Shutdown"
                    self.turtle.shutdown()
                    self.close()
                elif msg == chr(2):
                    print "Move forward."
                    self.turtle.move(ord(msg))
                    self.socket.send(self.turtle.get_odometry())
                elif msg == chr(3):
                    print "Turn right."
                    self.turtle.move(ord(msg))
                    self.socket.send(self.turtle.get_odometry())
                elif msg == chr(4):
                    print "Turn left."
                    self.turtle.move(ord(msg))
                    self.socket.send(self.turtle.get_odometry())
                elif msg == chr(5):
                    print "Wait."
                    self.turtle.move(ord(msg))
                    self.socket.send(self.turtle.get_odometry())
                # Testing commands.
                elif msg == chr(6):
                    x = float(ord(self.socket.recv(1)))/10-1
                    y = float(ord(self.socket.recv(1)))/10-1
                    z = float(ord(self.socket.recv(1)))/10-1
                    rz = float(ord(self.socket.recv(1)))/10-1
                    self.turtle.manually_move(x, y, z, rz)
                elif msg == chr(7):
                    self.socket.send(self.turtle.get_odometry())
                elif msg == chr(8):
                    print "Land."
                    self.turtle.land()
                elif msg == chr(9):
                    print "Takeoff."
                    self.turtle.initialize()

            except socket.timeout:
                pass
            except socket.error, err:
                print err
                self.close()
            except KeyboardInterrupt:
                print "Interrupted."
                self.close()

    def close(self):
        '''
        Close the connection and stop the running thread.
        '''
        print "TurtleClient: Shutdown."
        self.running = False
        self.drone.shutdown()
        self.socket.close()
        print "TurtleClient: Socket closed."

if __name__ == '__main__':
    CLIENT = DroneClient()
