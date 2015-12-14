"""
sensor.py: base class for any sensor like xtion

author: Nils Bernhardt
"""

import abc
from breezyslam.components import Laser


class Sensor(Laser):
    def __init__(self, width, scan_rate_hz, viewangle, distance_no_detection_mm, detectionMargin, offsetMillimeters):
        Laser.__init__(self, width, scan_rate_hz, viewangle, distance_no_detection_mm, detectionMargin,
                       offsetMillimeters)

    abc.abstractmethod
    def scan(self):
        """Return a scan array"""
        return

    abc.abstractmethod
    def shutdown(self):
        """Shutdown everything"""
        return
