import socket
import threading
from vehicle import Vehicle
#from turtlebot import Turtlebot

#HOST = '192.168.1.108'
HOST = ""
PORT = 8888

class Client(threading.Thread):
	
	running = True
	
	def __init__(self, vehicle):
		threading.Thread.__init__(self)
		self.robot = vehicle
		self.start()

	def run(self):
		'''
		Main loop
		'''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((HOST, PORT))
		
		while self.running:
			msg = self.socket.recv(1)

			if msg == "0":
				#self.robot.initialize()
				print "Initialize"
			elif msg == "1":
				self.close()
			elif msg == "2":
				#self.robot.move()
				print "Move forward"
			elif msg == "3":
				#self.robot.turn(1)
				print "Turn right"
			elif msg == "4":
				#self.robot.turn(-1)
				print "Turn left"
				
	def close(self):
		'''
		Close the connection and stop the running thread.
		'''
		self.running = False
		self.robot.shutdown()
		self.socket.close()
		print "Socket closed"

if __name__ == '__main__':
        testBot = Vehicle()
        client = Client(testBot)
        

