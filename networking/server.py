import socket
import threading

HOST = ""
PORT = 8888

class Server(threading.Thread):
	
	running = True
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def run(self):
		'''
		Main loop
		'''
		self.setup()
		
		msg = ""
		while self.running:
			while ";" not in msg:
				msg += self.connection.recv(1024)
			commands = msg.split(";")
			if commands[len(commands)-1] == "":
				for i in range(0, len(commands)-1):
					detail = commands[i].split(",")
					if detail[0] == "odometry":
						# TODO: odometry command
						self.connection.send("0.1,1,1") # Only testing!
					elif detail[0] == "move":
						# TODO: move command
						dx = detail[1]
						print "Move by: ", dx
					elif detail[0] == "turn":
						# TODO: turn command
						dthata = detail[1]
						print "Turn by: ", dthata
				msg = ""
			else:
				msg = commands[len(commands)-1]
				           
	def setup(self):
		'''
		Setup a connection to a client on PORT.
		'''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print "Socket created"
		
		# Bind socket to local host and port
		try:
			self.socket.bind((HOST, PORT))
		except socket.error as msg:
			print "Bind failed. Error Code : " + str(msg[0]) + " Message " + msg[1]
			self.running = False
			
		if self.running:     
			print "Socket bind complete"
			
			# Start listening on socket
			self.socket.listen(1)
			print "Socket now listening"
			
			# Connect to the client
			try:
				self.connection, addr = self.socket.accept()
				print "Connected with " + addr[0] + ":" + str(addr[1])
			except socket.error, e:
				self.close()
				print "Socket closed"
				
	def close(self):
		'''
		Close the connection and stop the running thread.
		'''
		self.running = False
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()
		print "Socket closed"

if __name__ == '__main__':
	server = Server()

