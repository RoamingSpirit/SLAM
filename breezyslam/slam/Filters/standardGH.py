from sFilter import sFilter
from filterinterface import FilterInterface

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

class standardGH(sFilter):
    def __init__(self, g,h,val=0,dval=0):
        """
            This instantiated a standard GH filter that updates itself over time
            as the data changes. it keeps a constant G and H value, but the
            internal coefficients change over time. 

        """
        self._name_ = "StandardGH_Filter"
        self.g = g
        self.h = h
        self._val = val
        self._dval = dval
        self._checkInit() ## Safety check


    def _checkInit(self):
        sFilter._checkInit(self)
        #print self._name_+"Initialized"


            

    def __call__(self, z, dt, g=None, h=None):
    	"""

    	:param z: This is the 'data' for the filter
    	:param dt: This is the timestep since the last run
    	:param g: Possible g value for the GH filter
    	:param h: Possible h value for the GH filter
    	:return:
    	"""
        if g is None: g = self.g
        if h is None: h = self.h

        ### Prediction Step
        v_est = self._val + dt*self._dval
        ## self._dval = self._dval ## Not Necesary to type

        ### Update Step
        residual = z - v_est
        self._dval = self._dval + h*residual/dt
        self._val = v_est + g*residual

        return self._val




        
    	
        

        
