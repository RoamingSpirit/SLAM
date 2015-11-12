# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "lukas"
__date__ = "$11.11.2015 11:10:27$"

from drone import Drone
import time

if __name__ == "__main__":
    ardrone = Drone()
    ardrone.run()
    
    """
    now = time.time()
    old = time.time()
    dt = now-old
    time_tup=(dt,now)
    print time_tup"""
    
