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
		"""
		Main loop
		"""
		self.setup()
        
		while self.running:
			msg = self.connection.recv(1024)
			if msg == "odometry":
				self.connection.send("0.1,1,1")
			elif msg == "move":
				dx = self.connection.recv(1024)
				print dx
			elif msg == "turn":
				dthata = self.connection.recv(1024)
				print dthata
           
	def setup(self):
		'''
		Setup a connection to a client on PORT.
		'''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print 'Socket created'
         
        # Bind socket to local host and port
		try:
			self.socket.bind((HOST, PORT))
		except socket.error as msg:
			print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			self.running = False
            
		if self.running:     
			print 'Socket bind complete'
             
            # Start listening on socket
			self.socket.listen(1)
			print 'Socket now listening'
             
            # Connect to the client
			try:
				self.connection, addr = self.socket.accept()
				print 'Connected with ' + addr[0] + ':' + str(addr[1])
			except socket.error, e:
				self.close()
				print 'Socket closed'
            
	def close(self):
		'''
		Close the connection and stop the running thread.
		'''
		self.running = False
		self.socket.shutdown(socket.SHUT_RDWR)
		self.socket.close()

if __name__ == '__main__':
	server = Server()

