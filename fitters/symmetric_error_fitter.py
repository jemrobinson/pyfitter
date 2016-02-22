from base_fitter import BaseFitter
import numpy as np
import scipy

class SymmetricErrorFitter(BaseFitter) :
  '''Fit data with symmetric errors'''
  def __init__( self, x, y, ey, *args, **kwargs ) :
    super(SymmetricErrorFitter, self).__init__(*args,**kwargs)
    self.x = np.array( x )
    self.y = np.array( y )
    self.ey = np.array( ey )


  def _update_chisq_ndof( self ) :
    '''Inherited from base class: update chi^2 and ndof'''
    self._chi_squared = np.sum( np.square( (self.y_predicted() - self.y) / self.ey ) )
    self._ndof = len(self.x) - len(self.fit_parameters)


  def _fit( self, initial_parameters ) :
    '''Inherited from base class: fit data with function'''
    x, y, ey = zip( *( (_x,_y,_ey) for _x, _y, _ey in zip(self.x,self.y,self.ey) if _ey != 0 ) )
    self._fit_parameters, self._covariance = scipy.optimize.curve_fit( self._function, x, y, sigma=ey, p0=initial_parameters, absolute_sigma=True )
