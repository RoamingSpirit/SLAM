import socket

HOST = ""
PORT = 8888

class Odometry_Client():

	def __init__(self):
		"""
		Initialize the client and connect to the server.
		"""
		self.socket = socket.socket()          
		self.socket.connect((HOST, PORT))
		print "Connected."
		
	def get_odometry(self):
		self.socket.send("odometry")
		data = self.socket.recv(1024)
		tuple = data.split(",", 3)
		return tuple
	
	def close(self):
		self.socket.close()     

if __name__ == '__main__':
	socket = Odometry_Client()
	print socket.get_odometry()
	socket.close()

