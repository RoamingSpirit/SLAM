import socket

HOST = ""
PORT = 8888

class Turtlebot():

	def __init__(self):
		"""
		Initialize the client and connect to the server.
		"""
		self.socket = socket.socket()          
		self.socket.connect((HOST, PORT))
		print "Connected."
		
	def getOdometry(self):
		self.socket.send("odometry")
		data = self.socket.recv(1024)
		tuple = data.split(",", 3)
		return tuple
	
	def close(self):
		self.socket.close()
		
	def move(self, dx):
		self.socket.send("move") 
		self.socket.send(str(dx)) 
		
	def turn(self, dthata):
		self.socket.send("turn") 
		self.socket.send(str(dthata)) 

if __name__ == '__main__':
	socket = Turtlebot()
	print socket.getOdometry()
	print socket.move(10)
	print socket.turn(90)
	socket.close()

