from GHBase import g_h_base


"""
This is a class representation of:
from gh_internal import plot_g_h_results

def g_h_filter(data, x0, dx, g, h, dt=1.):
    x = x0
    results = []
    for z in data:
        #prediction step
        x_est = x + (dx*dt)
        dx = dx

        # update step
        residual = z - x_est
        dx = dx    + h * (residual) / dt
        x  = x_est + g * residual     
        results.append(x)  
    return np.array(results)

"""

class standardGH(FilterInterface):
    def __init__(self, g, h):
        """
            This instantiated a standard GH filter that updates itself over time
            as the data changes. it keeps a constant G and H value, but the
            internal coefficients change over time. 

        """
        self._first = True
        self._x_mm, self._y_mm, self._theta_degrees = None, None, None
        self._dxy, self._dtheta = None, None
        
        self._g = g
        self._h = h
        self._dt = None
        print "Filter Instantiated"

    
    def _predict(self, data, step):
        pass

    def _update(self, data, step):
        pass


    def _fcall(self, slam_position, start_position, error, time, command):
        """
    	@Param: slam_position: Slam libraries next position, it is a position object from breezy slam
    	@Param, start_position: Odometry current position, it is a position object from breezy slam
    	@Param: error : float from 0 - 1 on how usefull the frame was. 0 == 0 error and 1 == all error
    	@Param: time : Change in time since last call <float> 
    	@Param: command : Not used so far

    	Position class:
    	<variable>.x_mm//.y_mm//.theta_degrees
    	"""
        slamX, slamY, slamTheta = slam_position.x_mm, slam_position.y_mm, slam_position.theta_degrees
        startX, startY, startTheta = start_position.x_mm, start_position.y_mm, start_position.theta_degrees

        diffX, diffY, diffTheta = abs(slamX-startX), abs(slamY-startY), abs(slamTheta-startTheta)

        ## if the system is turning

            
    	## if the system is driving straight


        ## if the system is stationary

            
            

    def __call__(self, slam_position, start_position, error, time, command):
    	"""
    	@Param: slam_position: Slam libraries next position, it is a position object from breezy slam
    	@Param, start_position: Odometry current position, it is a position object from breezy slam
    	@Param: error : float from 0 - 1 on how usefull the frame was. 0 == 0 error and 1 == all error
    	@Param: time : Change in time since last call <float> 
    	@Param: command : Not used so far

    	Position class:
    	<variable>.x_mm//.y_mm//.theta_degrees
    	"""
        ## if it's the furst run...
    	if self._first: return self._fcall(slam_position, start_position, error, time, command)

        slamX, slamY, slamTheta = slam_position.x_mm, slam_position.y_mm, slam_position.theta_degrees
        startX, startY, startTheta = start_position.x_mm, start_position.y_mm, start_position.theta_degrees

        

        ## if the system is stationary
    	
    	## if the system is turning

    	## if the system is driving straight
        
    	
        

        
