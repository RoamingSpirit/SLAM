"""
reader.py: Reads depth frames from the asus xtion/kinect

author: Nils Bernhardt
"""

from primesense import openni2
from primesense import _openni2 as c_api


class Reader:
    def __init__(self):
        path = '/home/pi/devel/OpenNI2/Packaging/OpenNI-Linux-Arm-2.2/Redist'
        openni2.initialize(path)  # can also accept the path of the OpenNI redistribution
        dev = openni2.Device.open_any()
        print dev.get_sensor_info(openni2.SENSOR_DEPTH)

        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320,
                               resolutionY=240, fps=30))
        self.depth_stream.start()

    def getHeight(self):
        """
        Return the stream height.
        :return: Stream height.
        """
        return 240  # todo

    def getWidth(self):
        """
        Return the stream width.
        :return: Stream width.
        """
        return 320  # todo

    def readFrame(self):
        """
        Read a new frame.
        :return: Data of frame.
        """
        frame = self.depth_stream.read_frame()
        data = frame.get_buffer_as_uint16()
        return data
