from filterinterface import FilterInterface
from sensorfilter import SensorFilter

class FilterHandler(FilterInterface):

    def __init__(self,xFilter = None, yFilter = None, thetaFilter = None):
        self.xFilter = xFilter
        self.yFilter = yFilter
        self.thetaFilter = thetaFilter
        self.dataFilter = SensorFilter()

    def __call__(slam_position, start_position, error, time, command):
        z_position = dataFilter(slam_position, start_position, error, time, command)
        est_position = z_position.copy()
        if(self.xFilter != None):
            est_position.x_mm = self.xFilter(...)
        if(self.yFilter != None):
            est_position.y_mm = self.yFilter(...)
        if(self.thetaFilter != None):
            est_position.tehta
        return est_position
