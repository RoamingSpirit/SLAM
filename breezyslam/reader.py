from primesense import openni2
from primesense import _openni2 as c_api
'''
reader.py: Reads depth frames from the asus xtion/kinect

author: Nils Bernhardt
'''
class Reader:
    
    def __init__(self):
        path = '/home/pi/devel/OpenNI2/Packaging/OpenNI-Linux-Arm-2.2/Redist'
        openni2.initialize(path)     # can also accept the path of the OpenNI redistribution
        dev = openni2.Device.open_any()
        print dev.get_sensor_info(openni2.SENSOR_DEPTH)

        self.depth_stream = dev.create_depth_stream()
        self.depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 320, resolutionY = 240, fps = 30))
        self.depth_stream.start()

    '''
    reurns the stream height
    '''
    def getHeight(self):
        return 240 #todo

    '''
    reurns the stream width
    '''
    def getWidth(self):
        return 320 #todo

    '''
    Reads a new frame.
    return: data of frame
    '''
    def readFrame(self):
        frame = self.depth_stream.read_frame()
        data = frame.get_buffer_as_uint16()
        return data
