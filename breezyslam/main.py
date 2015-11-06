'''
log2pgm.py : BreezySLAM Python demo.  Makes scans with an ASUS xtion and produces a .PGM image file showing robot 
             trajectory and final map.
             
For details see

    @inproceedings{coreslam-2010,
      author    = {Bruno Steux and Oussama El Hamzaoui}, modified by Nils Bernhardt
      title     = {CoreSLAM: a SLAM Algorithm in less than 200 lines of C code},
      booktitle = {11th International Conference on Control, Automation, 
                   Robotics and Vision, ICARCV 2010, Singapore, 7-10 
                   December 2010, Proceedings},
      pages     = {1975-1979},
      publisher = {IEEE},
      year      = {2010}
    }
                 
Copyright (C) 2014 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.

Change log:

20-APR-2014 - Simon D. Levy - Get params from command line
05-JUN-2014 - SDL - get random seed from command line
'''


from sensor import XTION

from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM

from progressbar import ProgressBar
from pgm_utils import pgm_save

from sys import exit, stdout
from time import time



# Map size, scale
MAP_SIZE_PIXELS          =  1000
MAP_SIZE_METERS          =  30
seed = 9999 #whit is this used for?
use_odometry = False #not yet implemented
iterations = 50 #how many scans to make


def main():
    #initialize the asus xtion as sensor
    sensor = XTION()
            
    # Create a CoreSLAM object with laser params and optional robot object
    slam = RMHC_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS, random_seed=seed) \
        if seed \
        else Deterministic_SLAM(sensor, MAP_SIZE_PIXELS, MAP_SIZE_METERS) 
    
    
    # Report what we're doing
    print('Processing %d scans with%s odometry / with%s particle filter...' % \
        (iterations, \
         '' if use_odometry else 'out', '' if seed else 'out'))
    progbar = ProgressBar(0, iterations, 80)
    
    # Start with an empty trajectory of positions
    trajectory = []

    # Start timing
    start_sec = time()
    
    # Loop over scans    
    for scanno in range(0, iterations):
    
        if use_odometry:
                  
            # Convert odometry to velocities
            velocities = robot.computeVelocities(odometries[scanno])
                                 
            # Update SLAM with lidar and velocities
            slam.update(sensor.scan(), velocities)
            
        else:
        
            # Update SLAM with lidar alone
            slam.update(sensor.scan())
                    
        # Get new position
        x_mm, y_mm, theta_degrees = slam.getpos()    
        
        # Add new position to trajectory
        trajectory.append((x_mm, y_mm))
        
        # Tame impatience
        progbar.updateAmount(scanno)
        stdout.write('\r%s' % str(progbar))
        stdout.flush()

    # Report elapsed time
    elapsed_sec = time() - start_sec
    print('\n%d scans in %f sec = %f scans / sec' % (iterations, elapsed_sec, iterations/elapsed_sec))
                    
                                
    # Create a byte array to receive the computed maps
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
    
    # Get final map    
    slam.getmap(mapbytes)
    
    # Put trajectory into map as black pixels
    for coords in trajectory:
                
        x_mm, y_mm = coords
                               
        x_pix = mm2pix(x_mm)
        y_pix = mm2pix(y_mm)
                                                                                              
        mapbytes[y_pix * MAP_SIZE_PIXELS + x_pix] = 0;
                    
    # Save map and trajectory as PGM file    
    pgm_save('test.pgm', mapbytes, (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
    
    print "done"

# Helpers ---------------------------------------------------------        

def mm2pix(mm):
        
    return int(mm / (MAP_SIZE_METERS * 1000. / MAP_SIZE_PIXELS))  


main()
