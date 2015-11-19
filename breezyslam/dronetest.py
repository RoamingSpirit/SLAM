from drone import Drone
import time


try:
    drone = Drone()
    drone.initialize()
    time.sleep(5)
    print 'rotate'
    drone.turn(90)
    time.sleep(2)
    drone.turn(-90)
    time.sleep(2)
    drone.turn(180)
    time.sleep(2)
    drone.shutdown()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Emergency shutdown.')
    drone.shutdown()
