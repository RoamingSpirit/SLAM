'''
Created on 17.11.2015

@author: Lukas
'''

import pygame, math
from drone import Drone

class Dronecontroller():
    def __init__(self, drone):
        # Pygame init
        pygame.init()
        
        # Initialize the drone
        self.drone = drone
        
        # Gamepad connecting
        j = pygame.joystick.Joystick(0)
        
        # Gamepad init
        j.init()
        
        def get(self):
            out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            it = 0 # Iterator
            pygame.event.pump()
            
            # Read input from the two joysticks       
            for i in range(0, j.get_numaxes()):
                out[it] = j.get_axis(i)
                it+=1
            # Read input from buttons
            for i in range(0, j.get_numbuttons()):
                out[it] = j.get_button(i)
                it+=1
    
            return out
    
        def run(self):
            running = True
            while running:
                # Get data
                but = get()
				
                if but[13] == 1:
                    running = False
                    drone.halt()
                    break
                elif but[4] == 1:
                    drone.takeoff()
                    print "Takeoff"
                elif but[6] == 1:
                    drone.land()
                    print "Land"
                hover = True
                
                # Clear small values
                for i in range(0, 4):
                    if math.fabs(but[i]) < 0.001:
                        but[i] = 0
                    else:
                        hover = False			
    			
    			# Send command to drone
    			drone.move(but[0], but[1], -but[3], but[2])

if __name__ == '__main__':
    main()


