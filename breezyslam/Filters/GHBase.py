
import abc

class g_h_base(object):
    """
        This is an abstract class for the definition of different g_h_ filters.
        The class works by instantiating an instance with any internal values
        to be set. Then using the __call__ method the system updates and returns
        the filtered values. The __call__ method to acvitely update the filter. 
    """
    def __init__(self):
        """
            Filter initialization
        """
        pass
    
    @abc.abstractmethod
    def _predict(self):
        """
            Does prediction for the filter
        """
        pass
    
    @abc.abstractmethod
    def _update(self):
        """
            Does updating for the filter
        """
        pass
    
    @abc.abstractmethod
    def __call__(self):
        """
            This is the 'active' method for the filter. If a filter is
            instantiated as f = somefilterClass(), then you can use the
            filter by using: f(). 
            
            Should look something like: 

            self._predict()
            self._update()
            return ... 
        """
        
