# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Lukas"
__date__ = "$03.11.2015 15:41:03$"

import socket

SERVER_ADDRESS = ('localhost', 10000)
BUFFER_SIZE = 1024
MESSAGE = "Success!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)

#Receive data
data = s.recv(BUFFER_SIZE)

s.send(MESSAGE)
s.close()

print "received data:", data
