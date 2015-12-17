"""
DroneClient class.
"""

import socket
import threading
from drone import Drone


class DroneClient(threading.Thread):
    """
    Class representing a client which receive drone commands
    and send drone odometry.
    """
    running = True

    def __init__(self, host="", port=9000):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.drone = Drone()
        self.socket = None
        self.start()

    def run(self):
        """
        Main loop.
        """
        print "DroneClient: Connecting.."
        connected = False
        while not connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.socket.settimeout(2)
                connected = True
            except socket.error:
                continue
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
                    self.socket.send(str(self.drone.getSize()))
                    self.socket.send("\n")
                elif msg == chr(1):
                    print "Shutdown"
                    self.drone.shutdown()
                    self.close()
                elif msg == chr(2):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                    self.drone.send("\n")
                elif msg == chr(3):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                    self.drone.send("\n")
                elif msg == chr(4):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                    self.drone.send("\n")
                elif msg == chr(5):
                    self.drone.move(ord(msg))
                    self.socket.send(self.drone.get_odometry())
                    self.drone.send("\n")
                # Testing commands.
                elif msg == chr(6):
                    self.drone.move(2)
                elif msg == chr(7):
                    self.drone.move(3)
                elif msg == chr(8):
                    self.drone.move(4)
                elif msg == chr(9):
                    self.drone.move(5)
                elif msg == chr(11):
                    self.drone.land()
                elif msg == chr(12):
                    self.drone.initialize()
                elif msg == chr(13):
                    self.socket.send(self.drone.get_odometry())
                    self.drone.send("\n")

            except socket.timeout:
                pass
            except socket.error, err:
                print err
                self.close()
            except KeyboardInterrupt:
                print "Interrupted."
                self.close()

    def close(self):
        """
        Close the connection and stop the running thread.
        """
        print "DroneClient: Shutdown."
        self.running = False
        self.drone.shutdown()
        self.socket.close()
        print "DroneClient: Socket closed."


if __name__ == '__main__':
    CLIENT = DroneClient()
