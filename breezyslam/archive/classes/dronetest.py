from drone import Drone
import time


try:
    drone = Drone()
    drone.initialize()
    time.sleep(10)
    drone.turn(90)
    x=0
    while(x<100):
	print drone.getOdometry()
        time.sleep(0.05)
	x+=1
    #drone.turn(-90)
    drone.shutdown()
except KeyboardInterrupt:
    print('\n\nKeyboard exception received. Emergency shutdown.')
    drone.shutdown()
