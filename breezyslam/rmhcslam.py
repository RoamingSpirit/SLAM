# distanceScanToMap is implemented as a C extension for efficiency
from pybreezyslam import distanceScanToMap

import pybreezyslam

import math
import time

# Basic params
_DEFAULT_MAP_QUALITY         = 50 # out of 255
_DEFAULT_HOLE_WIDTH_MM       = 600

# Random mutation hill-climbing (RMHC) params
_DEFAULT_SIGMA_XY_MM         = 100
_DEFAULT_SIGMA_THETA_DEGREES = 20
_DEFAULT_MAX_SEARCH_ITER     = 1000

from breezyslam.algorithms import SinglePositionSLAM, CoreSLAM

class RMHC_SLAM(SinglePositionSLAM):
    '''
    RMHC_SLAM implements the _getNewPosition() method of SinglePositionSLAM using Random-Mutation Hill-Climbing
    search.  Uses its own internal pseudorandom-number generator for efficiency.
    '''
    
    def __init__(self, laser, map_size_pixels, map_size_meters, 
                map_quality=_DEFAULT_MAP_QUALITY, hole_width_mm=_DEFAULT_HOLE_WIDTH_MM,
                random_seed=None, sigma_xy_mm=_DEFAULT_SIGMA_XY_MM, sigma_theta_degrees=_DEFAULT_SIGMA_THETA_DEGREES, 
                max_search_iter=_DEFAULT_MAX_SEARCH_ITER):
        '''
        Creates a RMHCSlam object suitable for updating with new Lidar and odometry data.
        laser is a Laser object representing the specifications of your Lidar unit
        map_size_pixels is the size of the square map in pixels
        map_size_meters is the size of the square map in meters
        quality from 0 through 255 determines integration speed of scan into map
        hole_width_mm determines width of obstacles (walls)
        random_seed supports reproducible results; defaults to system time if unspecified
        sigma_xy_mm specifies the standard deviation in millimeters of the normal distribution of 
           the (X,Y) component of position for RMHC search
        sigma_theta_degrees specifies the standard deviation in degrees of the normal distribution of 
           the rotational component of position for RMHC search
        max_search_iter specifies the maximum number of iterations for RMHC search
        '''
    
        SinglePositionSLAM.__init__(self, laser, map_size_pixels, map_size_meters, 
            map_quality, hole_width_mm)
            
        if not random_seed:
            random_seed = int(time.time()) & 0xFFFF
            
        self.randomizer = pybreezyslam.Randomizer(random_seed)
        
        self.sigma_xy_mm = sigma_xy_mm
        self.sigma_theta_degrees = sigma_theta_degrees
        self.max_search_iter = max_search_iter
        
    def update(self, scan_mm, velocities=None):

        if not velocities:
        
            velocities = (0, 0, 0)
    
        CoreSLAM.update(self, scan_mm, velocities)    
    
    def _getNewPosition(self, start_position):
        '''
        Implements the _getNewPosition() method of SinglePositionSLAM. Uses Random-Mutation Hill-Climbing
        search to look for a better position based on a starting position.
        '''     
        
        # RMHC search is implemented as a C extension for efficiency
        position = pybreezyslam.rmhcPositionSearch(
            start_position, 
            self.map, 
            self.scan_for_distance, 
            self.laser,
            self.sigma_xy_mm,
            self.sigma_theta_degrees,
            self.max_search_iter,
            self.randomizer)
                             
    def _random_normal(self, mu, sigma):
        
        return mu + self.randomizer.rnor() * sigma
