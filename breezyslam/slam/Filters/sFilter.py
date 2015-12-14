import abc


class sFilter(object):
    """
        This is an abstract class for the definition of different g_h_ filters.
        The class works by instantiating an instance with any internal values
        to be set. Then using the __call__ method the system updates and returns
        the filtered values. The __call__ method to acvitely update the filter. 
    """

    g = None
    h = None

    @abc.abstractmethod
    def __init__(self, g, h, val, dval):
        pass

    def _checkInit(self):
        if self.g is None or self.h is None:
            raise NotImplementedError("g and h not initialized properly")

    @abc.abstractmethod
    def __call__(self, z, dt, g, h):
        """
            This is the 'active' method for the filter. If a filter is
            instantiated as f = somefilterClass(), then you can use the
            filter by using: f(). 
            
            Should look something like: 

            self._predict()
            self._update()
            return ... 
        """
