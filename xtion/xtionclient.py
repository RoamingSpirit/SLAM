import socket
import threading
from xtion import XTION


class XtionClient(threading.Thread):

    def __init__(self, host="", port=10000):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.running = True
        self.host = host
        self.port = port
        self.xtion = XTION()
        self.start()

    def run(self):
        """
        Main loop.
        """
        self.socket.connect((HOST, PORT))

        while self.running:
            try:
                msg = self.socket.recv(1)
                if len(msg) == 0:
                    print "Connection to server lost."
                    self.close()
                elif msg == chr(1):
                    print "Shutdown"
                    self.close()
                elif msg == chr(2):
                    print "Scan."
                    scan = self.xtion.scan()
                    self.socket.send(self.turtle.get_odometry())

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
