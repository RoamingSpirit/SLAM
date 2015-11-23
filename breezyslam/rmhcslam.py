


from breezyslam.algorithms import RMHC_SLAM
import math


# Basic params
_DEFAULT_MAP_QUALITY         = 50 # out of 255
_DEFAULT_HOLE_WIDTH_MM       = 600

# Random mutation hill-climbing (RMHC) params
_DEFAULT_SIGMA_XY_MM         = 100
_DEFAULT_SIGMA_THETA_DEGREES = 20
_DEFAULT_MAX_SEARCH_ITER     = 1000

max_turn_speed = 10

class My_SLAM(RMHC_SLAM):
    
    def __init__(self, laser, map_size_pixels, map_size_meters, 
                map_quality=_DEFAULT_MAP_QUALITY, hole_width_mm=_DEFAULT_HOLE_WIDTH_MM,
                random_seed=None, sigma_xy_mm=_DEFAULT_SIGMA_XY_MM, sigma_theta_degrees=_DEFAULT_SIGMA_THETA_DEGREES, 
                max_search_iter=_DEFAULT_MAX_SEARCH_ITER):
        

       
    
        RMHC_SLAM.__init__(self, laser, map_size_pixels, map_size_meters, 
                map_quality, hole_width_mm,
                random_seed, sigma_xy_mm, sigma_theta_degrees, 
                max_search_iter)
            
       
    def update(self, scan_mm, velocities=None):
        self.errors=0
        self.values = len(scan_mm)
        for x in range(0, len(scan_mm)):
            if(scan_mm[x]==0):
                self.errors +=1
        RMHC_SLAM.update(self, scan_mm, velocities)    
    
    def _getNewPosition(self, start_position):   
        # RMHC search is implemented as a C extension for efficiency
        slam_position = RMHC_SLAM._getNewPosition(self, start_position)

        distx = slam_position.x_mm - start_position.x_mm
        disty = slam_position.y_mm - start_position.y_mm

        log = False

        if(math.sqrt(distx*distx+disty*disty)>50):
            log = True

        if(math.fabs(slam_position.theta_degrees - start_position.theta_degrees)>4):
            log = True

        if(log):
            print "\nError: ", self.errors
            print "Start ", start_position
            print "Slam ", slam_position
        
        #fslam = 1.5/self.values*(self.values-self.errors)-0.5
        fslam = float(self.values-self.errors)/self.values
        if(fslam<0):
            fslam=0
        elif(fslam>1):
            fslam=1
        fstart = 1-fslam


        if(slam_position.theta_degrees - start_position.theta_degrees > max_turn_speed):
            slam_position.theta_degrees = start_position.theta_degrees + max_turn_speed
            print "turn error"
        elif(start_position.theta_degrees - slam_position.theta_degrees > max_turn_speed):
            slam_position.theta_degrees = start_position.theta_degrees - max_turn_speed
            print "turn error"

        
        slam_position.theta_degrees = fslam * slam_position.theta_degrees + fstart * start_position.theta_degrees        
        slam_position.x_mm = fslam * slam_position.x_mm + fstart * start_position.x_mm
        slam_position.y_mm = fslam * slam_position.y_mm + fstart * start_position.y_mm

        if(log):
           print "Estimated ", slam_position
        
        return slam_position
                             
