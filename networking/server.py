import socket
from vehicle import Vehicle

HOST = ""
PORT = 8888

class Server(Vehicle):

	def getOdometry(self):
		'''
		Request and receive odometry
		'''
		self.connection.send("odometry\n")
		data = self.connection.recv(1024)
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
		self.connection.send("move,") 
		self.connection.send(str(dx))
		self.connection.send("\n")

	def turn(self, dtheta):
		'''
		Turn the TurtleBot by dtheta degree.
		'''
		self.connection.send("turn,") 
		self.connection.send(str(dtheta))
		self.connection.send("\n")

	def initialize(self):
		'''
		Iinitialize
		'''          
		self.setup()
		print "Connected."
		
	def setup(self):
		'''
		Setup a connection to a client on PORT.
		'''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Bind socket to local host and port
		try:
			self.socket.bind((HOST, PORT))
		except socket.error as msg:
			print "Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
		# Start listening on socket
		self.socket.listen(1)
		
		# Connect to the client
		try:
			self.connection, addr = self.socket.accept()
			print "Connected with " + addr[0] + ":" + str(addr[1])
		except socket.error, e:
			self.close()
			print "Socket closed"
			
	def shutdown(self):
		'''
		Close connection
		'''
		self.connection.send("close\n")
		self.connection.close()
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
		print "Connection closed."

if __name__ == '__main__':
	client = Server()
	client.initialize()
	print client.getOdometry()
	client.move(10)
	client.turn(90)
	client.shutdown()

