from filterinterface import FilterInterface
from sensorfilter import SensorFilter

class FilterHandler(FilterInterface):

    def __init__(self,xFilter = None, yFilter = None, thetaFilter = None):
        self.xFilter = xFilter
        self.yFilter = yFilter
        self.thetaFilter = thetaFilter
        self.dataFilter = SensorFilter()

    def __call__(self, slam_position, start_position, error, time, command):
        z_position = self.dataFilter(slam_position, start_position, error, time, command)
        est_position = z_position.copy()
        if(time == 0): return est_position
        
        if(self.xFilter != None):
            est_position.x_mm = self.xFilter(z_position.x_mm, time)
        if(self.yFilter != None):
            est_position.y_mm = self.yFilter(z_position.y_mm, time)
        if(self.thetaFilter != None):
            est_position.theta_degrees = self.thetaFilter(z_position.theta_degrees, time)
        
        return est_position
