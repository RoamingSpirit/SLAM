# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$11.11.2015 11:10:27$"

from droneconnect import DroneConnect

if __name__ == "__main__":
    ardrone = DroneConnect()
    ardrone.run()
