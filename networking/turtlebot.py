import socket
from vehicle import Vehicle

HOST = ""
PORT = 8888

class Turtlebot(Vehicle):
		
	def __init__(self):
		self.socket = socket.socket()
	
	def getOdometry(self):
		self.socket.send("odometry;")
		data = self.socket.recv(1024)
		tuple = data.split(",", 3)
		return tuple
	
	def close(self):
		'''
		Close the connection.
		'''
		self.socket.close()
		
	def move(self, dx):
		'''
		Move the TurtleBot by dx mm.
		'''
		self.socket.send("move,") 
		self.socket.send(str(dx))
		self.socket.send(";")
		
	def turn(self, dtheta):
		'''
		Turn the TurtleBot by dtheta degree.
		'''
		self.socket.send("turn,") 
		self.socket.send(str(dtheta))
		self.socket.send(";")
		
	def initialize(self):
		'''
		Iinitialize
		'''          
		self.socket.connect((HOST, PORT))
		print "Connected."

	def shutdown(self):
		'''
		Close connection
		'''
		self.socket.close()
		print "Connection closed."

if __name__ == '__main__':
	socket = Turtlebot()
	socket.initialize()
	print socket.getOdometry()
	socket.move(10)
	socket.turn(90)
	socket.close()

