'''
DroneClient class.
'''

import socket
import threading
from drone import Drone

class DroneClient(threading.Thread):
    '''
    Class representing a client which receive drone commands
    and send drone odometry.
    '''
    running = True

    def __init__(self, host = "", port = 9000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.drone = Drone()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.start()

    def run(self):
        '''
        Main loop
        '''
        print "DroneClient: Connecting.."
        self.socket.connect((self.host, self.port))
        print "DroneClient: Connected to host."

        while self.running:
            try:
                msg = self.socket.recv(1)
                if len(msg) == 0:
                    print "Connection to server lost."
                    self.close()
                elif msg == chr(10):
                    print "Emergency."
                    self.drone.emergency()
                elif msg == chr(0):
                    print "Initialize."
                    self.drone.initialize()
                    self.socket.send(chr(1))
                elif msg == chr(1):
                    print "Shutdown"
                    self.drone.shutdown()
                    self.close()
                elif msg == chr(2):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                elif msg == chr(3):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                elif msg == chr(4):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                elif msg == chr(5):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                # Testing commands.
                elif msg == chr(6):
                    x = float(ord(self.socket.recv(1)))/10-1
                    y = float(ord(self.socket.recv(1)))/10-1
                    z = float(ord(self.socket.recv(1)))/10-1
                    rz = float(ord(self.socket.recv(1)))/10-1
                    self.drone.manually_move(x, y, z, rz)
                elif msg == chr(7):
                    self.socket.send(self.drone.get_odometry())
                elif msg == chr(8):
                    self.drone.land()
                elif msg == chr(9):
                    self.drone.initialize()

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
        print "DroneClient: Shutdown."
        self.running = False
        self.drone.shutdown()
        self.socket.close()
        print "DroneClient: Socket closed."

if __name__ == '__main__':
    CLIENT = DroneClient()
