__author__ = 'Troy Hughes'

import serial
from serial import SerialTimeoutException


class SCommunicator(object):
    def __init__(self,COMPort):
        self._s = serial.Serial(COMPort,
                                baudrate=115200,
                                timeout = 3,
                                write_timeout = 0.1)
        self._port = COMPort
        self._s.open()


    def close(self):
        self._s.close()


    """ From here we need to define: GET and GIVE commands
    GET: Master send a specific command to the slave and wait for a response, timeout after X time.
    GIVE: Master will send a value to the slave and will not wait for a response.
    """

    def _safeSend(self, data, location):
        try: self._s.write(self,data)
        except SerialTimeoutException,e:
            print "Your error location is: "+location
            raise SerialTimeoutException("SCommunicatory on port: "+self._port+" has failed to write")

    def _safeRecv(self, size):
        data = self._s.read()

    def get(self,commandType, commandData):

        sendCommand = commandType+"::"+commandData

        self._safeSend(sendCommand, "SCommunicator.get")







    def ack(self):
        
        # try:self._s.write("|")
        #
        return


