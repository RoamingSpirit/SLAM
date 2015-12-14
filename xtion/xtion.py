"""
sensor.py : Asus xtion which emulates a laser scaner.

author: Nils Bernhardt
"""

from reader import Reader
from sensor import Sensor
import math


class XTION(Sensor):
    """
    A class for the Asus XTION.
    """
    viewangle = 58  # asus xtion view in degrees
    linecount = 5  # lines above and below to generate average (0=online desired line)
    distance_no_detection_mm = 3500  # max detection range
    scan_rate_hz = 23  # todo find value
    detectionMargin = 4  # pixels on the sites of the scans which should be ignored
    offsetMillimeters = 50  # offset of the sensor to the center of the robot

    def __init__(self, log=True):
        self.log = log
        if log:
            self.out = open('log', 'w')
        self.reader = Reader()
        self.width = self.reader.getWidth()
        self.height = self.reader.getHeight()

        self.row = self.height / 2  # row to read

        Sensor.__init__(self, self.width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm,
                        self.detectionMargin, self.offsetMillimeters)

    def get_parameters(self):
        parameters = [None] * 6
        parameters[0] = str(self.width)
        parameters[1] = str(self.scan_rate_hz)
        parameters[2] = str(self.viewangle)
        parameters[3] = str(self.distance_no_detection_mm)
        parameters[4] = str(self.detectionMargin)
        parameters[5] = str(self.offsetMillimeters)
        return parameters

    def scan(self):
        """
        Scan one line.
        :return: Array with the values.
        """
        frame = self.reader.readFrame()
        data = self.read_line(frame, self.width, self.height, self.row)
        return data

    def read_line(self, frame_data, width, height, line):
        """
        Print the depth value for every pixel in one line.
        :param frame_data: depth frame.
        :param width: width of the frame.
        :param height: height of the frame.
        :param line: line to print.
        :return: one data row converted as lidar.
        """
        data = []
        for x in range(width - 1, -1, -1):
            value = self.getAverageDepth(frame_data, width, height, x, line, self.linecount)
            converted = self.to_lidar_value(value, x, width)
            if self.log:
                self.out.write(str(converted) + ' ')
            data.append(str(converted))
        if self.log:
            self.out.write('\n')
        return data

    def to_lidar_value(self, value, x, width):
        """
        Convert the measured value of the asus xtion to the value a lidar would measure.
        :param value: value to convert.
        :param x: x position of the value.
        :param width: of the frame.
        :return: converted value.
        """
        angle = (float(width) / 2 - x) / width * self.viewangle
        return int(value / math.cos(math.radians(angle)))

    '''
    #get the average value of a specifiv pixel with a certain amount of pixel above and under.
    #frame_data - depth frame
    #widht -  width of the frame
    #height - height of the frame
    #x - coordinate of the pixel
    #y - coordinate of the pixel
    #distance - pixels under and above the desired row
    return: average value
    '''

    def getAverageDepth(self, frame_data, width, height, x, y, distance):
        """
        Get the average value of a specific pixel with a certain amount of pixel above and under.
        :param frame_data: Depth frame.
        :param width: Width of the frame.
        :param height: Height of th frame.
        :param x: X coordinate of the pixel.
        :param y: Y coordinate of the pixel.
        :param distance: Pixels under and above the desired row.
        :return: Average value.
        """
        sum = 0
        count = 0
        for yTemp in range(-distance + y, distance + 1 + y):
            value = frame_data[yTemp * width + x]
            if value > 0:
                sum += value
                count += 1
        if count > 0:
            return sum / count
        else:
            return 0


class FileXTION(XTION):
    """
    A class for reading the log file of an Asus XTION.
    """
    # current frame read
    index = 0

    def __init__(self, dataset, datadir='.'):
        """
        Initialization.
        :param dataset: Filename.
        :param datadir: Directory of the file default '.'.
        """
        self.scans, width = self.load_data(datadir, dataset)
        Sensor.__init__(self, width, self.scan_rate_hz, self.viewangle, self.distance_no_detection_mm,
                        self.detectionMargin, self.offsetMillimeters)

    def scan(self):
        """
        Read a scan.
        :return: Array with the values.
        """
        if self.index < len(self.scans):
            self.index += 1
            return self.scans[self.index - 1]
        else:
            return []

    def load_data(self, datadir, dataset):
        """
        Load a stored log file and saves the scans.
        :param datadir: directionary of the file.
        :param dataset: filename.
        :return: scans, width of the scans
        """
        filename = '%s/%s' % (datadir, dataset)
        print('Loading data from %s...' % filename)

        fd = open(filename, 'rt')

        scans = []

        while True:

            s = fd.readline()

            if len(s) == 0:
                break

            toks = s.split()[0:-1]  # ignore ''

            lidar = [int(tok) for tok in toks[:]]

            for x in range(0, len(lidar)):
                if lidar[x] > self.distance_no_detection_mm:
                    lidar[x] = 0

            scans.append(lidar)

        fd.close()

        return scans, len(scans[0])
