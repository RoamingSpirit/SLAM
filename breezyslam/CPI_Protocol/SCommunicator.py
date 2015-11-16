__author__ = 'Troy Hughes'

import serial


class SCommunicator(object):
    def __init__(self,COMPort):
        self._s = serial.Serial(COMPort, baudrate=115200)
        self._s.open()


    def close(self):
        self._s.close()


""" From here we need to define: GET and GIVE commands
GET: Master send a specific command to the slave and wait for a response, timeout after X time.
GIVE: Master will send a value to the slave and will not wait for a response.
"""