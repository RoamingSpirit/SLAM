"""
TurtleClient class.
"""

import socket
import threading
from turtlebot import Turtlebot


class TurtleClient(threading.Thread):
    """
    Class representing a client which receive turtlebot commands
    and send turtlebot odometry.
    """

    def __init__(self, host="", port=9000):
        threading.Thread.__init__(self)
        self.socket = None
        self.host = host
        self.port = port
        self.turtle = Turtlebot()
        self.running = True
        self.start()

    def run(self):
        """
        Main loop.
        """
        print "TurtleClient: Connecting.."
        connected = False
        while not connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.socket.settimeout(2)
                connected = True
            except socket.error:
                continue
        print "TurtleClient: Connected to host."

        while self.running:
            try:
                msg = self.socket.recv(1)
                if len(msg) == 0:
                    print "Connection to server lost."
                    self.close()
                elif msg == chr(0):
                    print "Initialize."
                    self.turtle.initialize()
                    self.socket.send(str(self.turtle.getSize()))
                    self.socket.send("\n")
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
                else:
                    print "Error: Invalid command!"

            except socket.timeout:
                pass
            except socket.error, error:
                print error
                self.close()
            except KeyboardInterrupt:
                print "Interrupted."
                self.close()

    def close(self):
        """
        Close the connection and stop the running thread.
        """
        print "TurtleClient: Shutdown."
        self.running = False
        self.turtle.shutdown()
        self.socket.close()
        print "TurtleClient: Socket closed."


if __name__ == '__main__':
    CLIENT = TurtleClient("192.168.0.100")
