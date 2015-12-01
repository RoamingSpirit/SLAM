__author__ = 'Troy Hughes'

import serial
from serial import SerialTimeoutException
import time

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
        try: self._send(data)
        except SerialTimeoutException,e:
            print "Your error location is: "+location
            raise SerialTimeoutException("SCommunicatory on port: "+self._port+" has failed to write")

    def _safeRecv(self, size, timeout=1, size_known=True):
        try: data = self._recv(size, timeout, size_known)
        except RuntimeError,e:
            raise e
        return data

    def getData(self,commandType, commandData):
        sendCommand = commandType+"::"+commandData
        self._safeSend(sendCommand, "SCommunicator.getData")

        if not self.recvAck():
            raise RuntimeError("Ack Dropped from getData Function")
        data = self._safeRecv(None,None,False)
        self.ack()
        return

    def sendData(self,data):
        sData = str(data)
        sData = sData + '\r\n'

        self._safeSend(sData,'SendData')
        return



    def ack(self):
        self._safeSend('!',"ACK_Send")

    def recvAck(self):
        data = self._safeRecv(1)
        if data == '!':
            return True
        else:
            return False


    def _send(self,value):
        self._s.write(value)
        return

    def _recv(self,size, timeout, size_known=True):
        if size_known:
            start_time = time.time()
            while ((time.time() - start_time <= timeout) and self._s.inWaiting() < size):
                continue
            if time.time() - start_time <= timeout:
                raise RuntimeError("Timout while trying to _recv")
            return self._s.read(size)
        else:
            data = self._s.readline()
            print data
            return data

