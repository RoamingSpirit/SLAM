"""
author: Nils Bernhardt
Class for reading the odometry log from a file.
"""
from vehicle import Vehicle


class FileDrone(Vehicle):
    index = 0

    def __init__(self, dataset, datadir='.'):
        self.data = self.load_data(datadir, dataset)

    def initialize(self):
        pass

    @staticmethod
    def load_data(datadir, dataset):
        """
        Load a stored log file and saves the scans.
        :param datadir: Directory of the file.
        :param dataset: Filename.
        :return: Scans, width of the scans.
        """
        filename = '%s/%s' % (datadir, dataset)
        print('Loading odometry from %s...' % filename)

        fd = open(filename, 'rt')

        data = []

        while True:

            s = fd.readline()

            if len(s) == 0:
                break

            toks = s.split()[:]  # ignore ''

            odometry = [float(tok) for tok in toks[:]]

            data.append(odometry)

        fd.close()

        return data

    def getOdometry(self):
        """
        Return a tuple of odometry.
        :return: Dxy in mm, dthata in degree, dt in s
        """
        if self.index >= len(self.data):
            return 0, 0, 0
        else:
            self.index += 1
            return self.data[self.index - 1]

    def move(self, cmd):
        """
        Set the moving command.
        """
        return self.getOdometry()

    def getSize(self):
        # TODO return size in meter
        return 0.4

    def shutdown(self):
        """
        Nothing todo
        """
        return
