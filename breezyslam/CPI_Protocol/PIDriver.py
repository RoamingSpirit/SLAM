__author__ = 'Troy Hughes'

from SCommunicator import SCommunicator

class PIDriver():
    def __init__(self,COMPort):
        self._c = SCommunicator(COMPort)


    """ http://pyserial.readthedocs.org/en/latest/pyserial_api.html """
    """ The above API can explain how these functions will work.
    """
    def drive(self, distance):
        """
        Sends a drive command to the serial port that this is connected to
        :param distance:
        :return:
        """

        """
            Will send a command value and wait for a confirmation bit.
        """
        return

    def turn(self, angle):
        """
        Sends a turn command to the serial port that this is connected to
        :param angle:
        :return:
        """
        """
            Will send a command value and wait for a confirmation bit.
        """
        return

    def getOdom(self):
        """ Sends a data command to the serial port that this is connected to
        :return:
        """
        """
            Will send a command and wait for the confirmation. Then will
            wait for the odom data, followed by another confirmation.
            This will then return a confirmation message.
        """
        return


