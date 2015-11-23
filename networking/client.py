import socket
import threading
from vehicle import Vehicle

HOST = ""
PORT = 8888

class Client(threading.Thread):
	
	running = True
	
	def __init__(self):
		threading.Thread.__init__(self)
		#self.robot = vehicle
		self.start()

	def run(self):
		'''
		Main loop
		'''
		self.socket = socket.socket()
		self.socket.connect((HOST, PORT))
		
		msg = ""
		while self.running:
			while "\n" not in msg:
				msg += self.socket.recv(1024)
			commands = msg.split("\n")

			for i in range(0, len(commands)-1):
				detail = commands[i].split(",")
				if detail[0] == "initialize":
					#self.robot.initialize()
					print "Initialize."
				elif detail[0] == "odometry":
					#self.robot.getOdometry()
					self.socket.send("0.1,1,1") # Only testing!
				elif detail[0] == "move":
					#self.robot.move(detail[1])
					print "Move by: ", detail[1]
				elif detail[0] == "turn":
					#self.robot.move(detail[1])
					print "Turn by: ", detail[1]
				elif detail[0] == "close":
					self.close()
					
				msg = commands[len(commands)-1]
				           
	
				
	def close(self):
		'''
		Close the connection and stop the running thread.
		'''
		self.running = False
		#self.robot.shutdown()
		self.socket.close()
		print "Socket closed"

if __name__ == '__main__':
	client = Client()

