import serial
import time

import sys
import signal
"""

======================LiDAR Commands===============================
ShowConfig    - Show the running configuration
SaveConfig    - Save the running configuration to EEPROM
ResetConfig   - Restore the original configuration
SetRPM        - Set the desired rotation speed (min: 200, max: 300)
SetKp         - Set the proportional gain
SetKi         - Set the integral gain
SetKd         - Set the derivative gain
SetSampleTime - Set the frequency the PID is calculated (ms)
ShowRPM       - Show the rotation speed
HideRPM       - Hide the rotation speed
ShowDist      - Show the distance data
HideDist      - Hide the distance data
ShowAngle     - Show distance data for a specific angle (0 - 359 or 360 for all)
MotorOff      - Stop spinning the lidar
MotorOn       - Enable spinning of the lidar
HideRaw       - Stop outputting the raw data from the lidar
ShowRaw       - Enable the output of the raw lidar data
"""


    
def signal_handler(signal, frame):
    print "Exiting"
    arduCom.close()
    sys.exit(0)
    
    
print "Beginning program..."

arduCom = serial.Serial(port ='COM8', baudrate = 115200)


signal.signal(signal.SIGINT, signal_handler)


stringList = ""
flaggy = 0
arduCom.write("ShowDist\n")
while True:

    if arduCom.inWaiting() > 0:
        inByte = arduCom.readline()
        print inByte 
       
    flaggy += 1

    if flaggy == 100000:
        print "made it!"
        arduCom.write("ShowDist\n")
               
arduCom.close()

