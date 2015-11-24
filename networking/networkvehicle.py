import socket
from vehicle import Vehicle

HOST = ""
PORT = 8888

MOVE_FORWARD = 2
TURN_RIGHT = 3
TURN_LEFT = 4

class NetworkVehicle(Vehicle):
	
	def move(self, cmd):
		if cmd == MOVE_FORWARD:
			self.connection.send(str(MOVE_FORWARD))
		elif cmd == TURN_RIGHT:
			self.connection.send(str(TURN_RIGHT))
		elif cmd == TURN_LEFT:
			self.connection.send(str(TURN_LEFT))

	def getOdometry(self):
		'''
		Request and receive odometry
		'''
		self.connection.send("odometry\n")
		data = self.connection.recv(1024)
		tuple = data.split(",", 3)
		return tuple

	def initialize(self):
		'''
		Iinitialize
		'''          
		self.setup()
		#self.connection.send("0")
		print "Connected."
			
	def shutdown(self):
		'''
		Close connection
		'''
		self.connection.send("1")
		self.connection.close()
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
		print "Connection closed."
		
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

if __name__ == '__main__':
	client = NetworkVehicle()
	client.initialize()
	client.move(MOVE_FORWARD)
	client.move(TURN_LEFT)
	client.shutdown()

