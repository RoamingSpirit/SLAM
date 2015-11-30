from filterinterface import FilterInterface
import math

class SensorFilter(FilterInterface):
        
    def __call__(self, slam_position, start_position, error, time, commandself):
        distx = slam_position.x_mm - start_position.x_mm
        disty = slam_position.y_mm - start_position.y_mm

        log = False

        est_position = slam_position.copy()
        if(math.sqrt(distx*distx+disty*disty)>50):
            log = True

        if(math.fabs(slam_position.theta_degrees - start_position.theta_degrees)>4):
            log = True

        if(log):
            print "\nError: ", error
            print "Start ", start_position
            print "Slam ", slam_position
        
        fslam = 1-1.5*error
        
        
        if(fslam<0):
            fslam=0
        elif(fslam>1):
            fslam=1
        fstart = 1-fslam


        if(slam_position.theta_degrees - start_position.theta_degrees > self.max_turn_speed):
            slam_position.theta_degrees = start_position.theta_degrees + self.max_turn_speed
            print "turn error"
        elif(start_position.theta_degrees - slam_position.theta_degrees > self.max_turn_speed):
            slam_position.theta_degrees = start_position.theta_degrees - self.max_turn_speed
            print "turn error"

        
        est_position.theta_degrees = fslam * slam_position.theta_degrees + fstart * start_position.theta_degrees        
        est_position.x_mm = fslam * slam_position.x_mm + fstart * start_position.x_mm
        est_position.y_mm = fslam * slam_position.y_mm + fstart * start_position.y_mm

        if(log):
           print "Estimated ", est_position
        return est_position

