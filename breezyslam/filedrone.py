
from vehicle import Vehicle

class FileDrone(Vehicle):

    index = 100

    def __init__(self, dataset, datadir = '.'):
        self.data = self.load_data(datadir, dataset)

    '''
    loads a stroed log file and saves the scans.
    datadir: directionary of the file
    dataset: filename
    return: scans, width of the scans
    '''
    def load_data(self, datadir, dataset):
        
        filename = '%s/%s' % (datadir, dataset)
        print('Loading odometry from %s...' % filename)
        
        fd = open(filename, 'rt')
        
        data = []
        
        while True:  
            
            s = fd.readline()
            
            if len(s) == 0:
                break       
                
            toks = s.split()[:] # ignore ''
                            
            odometry = [float(tok) for tok in toks[:]]
            

            data.append(odometry)
            
        fd.close()
            
        return data

        
    def getOdometry(self):
        """
        return a tuple of odometry (dxy in mm,dthata in degree, dt in s)
        """
	if(self.index >= len(self.data)):
            return 0,0,0
        else:
            self.index += 1
            return self.data[self.index - 1]
