import socket
import threading
from vehicle import Vehicle
from turtlebot import Turtlebot

HOST = '192.168.1.108'
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
		
		msg = ""
		while self.running:
			while "\n" not in msg:
				msg += self.socket.recv(1024)
			commands = msg.split("\n")

			for i in range(0, len(commands)-1):
				detail = commands[i].split(",")
				if detail[0] == "initialize":
					self.robot.initialize()
					print "Initialize."
				elif detail[0] == "odometry":
					self.socket.send(str(self.robot.getOdometry())) # Only testing!
				elif detail[0] == "move":
					self.robot.move(float(detail[1]))
					print "Move by: ", detail[1]
				elif detail[0] == "turn":
					self.robot.turn(-float(detail[1]))
					print "Turn by: ", detail[1]
				elif detail[0] == "close":
					self.close()
					
				msg = commands[len(commands)-1]
				           
	
				
	def close(self):
		'''
		Close the connection and stop the running thread.
		'''
		self.running = False
		self.robot.shutdown()
		self.socket.close()
		print "Socket closed"

if __name__ == '__main__':
        testBot = Turtlebot()
        client = Client(testBot)
        

