"""
author: Nils Bernhardt
Class which performs a rmhc slam and gives the possibility to apply g-h filter.
"""

from breezyslam.algorithms import RMHC_SLAM
from Filters.filterhandler import FilterHandler
from Filters.standardGH import standardGH
import math

# Basic params
_DEFAULT_MAP_QUALITY = 100  # out of 255
_DEFAULT_HOLE_WIDTH_MM = 400

# Random mutation hill-climbing (RMHC) params
_DEFAULT_SIGMA_XY_MM = 20  # w/out odometry 45
_DEFAULT_SIGMA_THETA_DEGREES = 1  # w/out odometry 2.5
_DEFAULT_MAX_SEARCH_ITER = 1000  # w/out odometry 1000

# Filter
filtering = False
g = 0.1
h = 0.1

#maximal turning speed
MAX_DEGREE_PER_S = 360.0


class My_SLAM(RMHC_SLAM):
    def __init__(self, laser, map_size_pixels, map_size_meters,
                 map_quality=_DEFAULT_MAP_QUALITY, hole_width_mm=_DEFAULT_HOLE_WIDTH_MM,
                 random_seed=None, sigma_xy_mm=_DEFAULT_SIGMA_XY_MM, sigma_theta_degrees=_DEFAULT_SIGMA_THETA_DEGREES,
                 max_search_iter=_DEFAULT_MAX_SEARCH_ITER):

        self.myfilter = FilterHandler(standardGH(g, h, 20000, 0), standardGH(g, h, 20000, 0), standardGH(g, h))

        RMHC_SLAM.__init__(self, laser, map_size_pixels, map_size_meters,
                           map_quality, hole_width_mm,
                           random_seed, sigma_xy_mm, sigma_theta_degrees,
                           max_search_iter)

    def update(self, scan_mm, velocities=None, command=0):
        """
        Calculates the amount of usefull pixels perframe and stores the time.
        scan_mm: new scan
        velocities: velocitie data
        command: next to perform command
        :param velocities:
        :param command:
        :param scan_mm:
        """
        errors = 0
        self.values = len(scan_mm)
        for x in range(0, len(scan_mm)):
            if scan_mm[x] == 0:
                errors += 1 
        self.error = float(errors) / len(scan_mm)
        if velocities == None:
            self.time = None
        else:
            self.time = velocities[2]
        self.command = command
        RMHC_SLAM.update(self, scan_mm, velocities)

    def _getNewPosition(self, start_position):
        """
        Filters the rmhc slam result.
        start_position: estimated position based on odometry
        """
        # RMHC search is implemented as a C extension for efficiency
        slam_position = RMHC_SLAM._getNewPosition(self, start_position)
        
        #check slam values for reliable turn.
        #vtheta = (slam_position.theta_degrees - start_position.theta_degrees)/self.time
        #if(math.fabs(vtheta) > MAX_DEGREE_PER_S):
        #    vtheta = vtheta/math.fabs(vtheta) * MAX_DEGREE_PER_S
        #    slam_position.theta_degrees = start_position.theta_degrees + vtheta * self.time
        
        
        if not filtering: return slam_position
        if self.time == None:
            return slam_position
        return self.myfilter(slam_position, start_position, self.error, self.time, self.command)
