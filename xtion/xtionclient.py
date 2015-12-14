"""
xtionclient.py: Class representing a connection to a 'NetworkVehicle.'

author: Lukas Brauckmann
"""

import socket
from xtion import XTION


class XtionClient:

    def __init__(self, host="", port=9001):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.running = True
        self.host = host
        self.port = port
        self.xtion = XTION()
        self.run()

    def run(self):
        """
        Main loop.
        """
        self.socket.connect((self.host, self.port))

        while self.running:
            try:
                msg = self.socket.recv(1)
                if len(msg) == 0:
                    print "SensorClient: Connection to server lost."
                    self.close()
                elif msg == chr(0):
                    print "SensorClient: Initialize."
                    parameters = self.xtion.get_parameters()
                    msg = ",".join(parameters)
                    self.socket.send(msg)
                    self.socket.send("\n")
                elif msg == chr(1):
                    print "SensorClient: Shutdown"
                    self.close()
                elif msg == chr(2):
                    print "SensorClient: Scan."
                    scan = self.xtion.scan()
                    msg = ",".join(scan)
                    self.socket.send(msg)
                    self.socket.send('\n')

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
        self.running = False
        self.socket.close()
        print "Socket closed"


if __name__ == '__main__':
    client = XtionClient()
