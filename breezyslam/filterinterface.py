'''
author: Nils Bernhardt 
'''

import abc

class FilterInterface(object):

    abc.abstractmethod
    def __call__(slam_position, start_position, error, time, command):
        """return the estimated position"""
        return

    
