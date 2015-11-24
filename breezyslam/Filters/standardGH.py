from GHBase import g_h_base


"""
This is a class representation of:
from gh_internal import plot_g_h_results

def g_h_filter(data, x0, dx, g, h, dt=1.):
    x = x0
    results = []
    for z in data:
        #prediction step
        x_est = x + (dx*dt)
        dx = dx

        # update step
        residual = z - x_est
        dx = dx    + h * (residual) / dt
        x  = x_est + g * residual     
        results.append(x)  
    return np.array(results)

"""

class standardGH(g_h_base):
    def __init__(self, dstart, dchangeStart, g, h, dt=0.1):
        """
            This instantiated a standard GH filter that updates itself over time
            as the data changes. it keeps a constant G and H value, but the
            internal coefficients change over time. 

        """
        self._x0 = dstart
        self._dx = dchangeStart
        self._g = g
        self._h = h
        self._dt = dt
        print "Filter Instantiated"

    
    def _predict(self, data, step):
        pass

    def _update(self, data, step):
        pass

    def __call__(self, data):
        self._predict()
        self._update()
        

        
