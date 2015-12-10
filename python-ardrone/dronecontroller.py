'''
Created on 17.11.2015

@author: Lukas
'''

import pygame, math, time
import libardrone

class DroneController():
    def __init__(self):
        # Pygame init
        pygame.init()
        
        self.drone = libardrone.ARDrone()
        print "Connected to drone."
        
        # Gamepad connecting
        self.j = pygame.joystick.Joystick(0)
        
        # Gamepad init
        self.j.init()
        print "Initialized."
        
        self.running = True
        self.hover = True
        
    def get(self):
        out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        it = 0 # Iterator
        pygame.event.pump()
        
        # Read input from the two joysticks       
        for i in range(0, self.j.get_numaxes()):
            out[it] = self.j.get_axis(i)
            it+=1
        # Read input from buttons
        for i in range(0, self.j.get_numbuttons()):
            out[it] = self.j.get_button(i)
            it+=1

        return out
    
    def run(self):
        while self.running:
            print self.drone.navdata.get(0, dict()).get('psi', 0)
            # Get data
            but = self.get()

            if but[13] == 1:
                self.running = False
                self.drone.halt()
                break
            elif but[4] == 1:
                self.drone.takeoff()
                print "Takeoff"
            elif but[6] == 1:
                self.drone.land()
                print "Land"
            #~ 
            # Clear small values
            for i in range(0, 4):
                if math.fabs(but[i]) < 0.01:
                    but[i] = 0
                else:
                    self.hover = False
 
            if self.hover:
                self.drone.hover()
            else:
                # Send command to drone
                self.drone.move(but[0], but[1], -but[3], but[2])
            
    def emergency(self):
        self.running = False
        #self.drone.reset()
        self.drone.halt()

if __name__ == '__main__':
    controller = DroneController()
    controller.run()
    var = raw_input("Please enter something: ")
    print "you entered", var
    controller.emergency()
