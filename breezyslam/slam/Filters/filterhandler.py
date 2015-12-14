"""
author: Nils Bernhardt
Class which handles the filters for the different values.


"""
from filterinterface import FilterInterface


class FilterHandler(FilterInterface):
    def __init__(self, xFilter=None, yFilter=None, thetaFilter=None):
        """
        Initialization.
        :param xFilter:
        :param yFilter:
        :param thetaFilter:
        """
        self.xFilter = xFilter
        self.yFilter = yFilter
        self.thetaFilter = thetaFilter

    def __call__(self, slam_position, start_position, error, time, command):
        """
        Filters the position
        slam_position: calculated position
        start_position: position based on odometry
        error: useful pixels
        time: time ellapsed
        command: command to perform
        """
        est_position = slam_position.copy()
        if time == 0: return est_position

        if self.xFilter != None:
            est_position.x_mm = self.xFilter(z_position.x_mm, time)
        if self.yFilter != None:
            est_position.y_mm = self.yFilter(z_position.y_mm, time)
        if self.thetaFilter != None:
            est_position.theta_degrees = self.thetaFilter(z_position.theta_degrees, time)

        return est_position
