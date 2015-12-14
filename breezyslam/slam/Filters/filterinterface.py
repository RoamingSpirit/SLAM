"""
author: Nils Bernhardt
"""

import abc


class FilterInterface(object):
    max_turn_speed = 10

    abc.abstractmethod

    def __call__(slam_position, start_position, error, time, command):
        """return the estimated position"""
        return
