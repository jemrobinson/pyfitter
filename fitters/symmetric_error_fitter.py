from base_fitter import BaseFitter
from scipy.optimize import curve_fit

class SymmetricErrorFitter(BaseFitter) :
  '''Fit data with symmetric errors'''
  def __init__( self, x, y, ey, *args, **kwargs ) :
    super(SymmetricErrorFitter, self).__init__(*args,**kwargs)
    self.x = x
    self.y = y
    self.ey = ey


  def _update_chisq_ndof( self, function ) :
    '''Inherited from base class: update chi^2 and ndof'''
    self._chi_squared, self._ndof = 0, 0
    for x, y, ey in zip(self.x, self.y, self.ey) :
      if ey == 0 : continue
      self._chi_squared += ( (y - function(x,*self.fit_parameters)) / ey )**2
      self._ndof += 1
    self._ndof -= len(self.fit_parameters)


  def _fit( self, function, initial_parameters ) :
    '''Inherited from base class: fit data with function'''
    x, y, ey = zip( *( (_x,_y,_ey) for _x, _y, _ey in zip(self.x,self.y,self.ey) if _ey != 0 ) )
    self._fit_parameters, self._covariance = curve_fit( function, x, y, sigma=ey, p0=initial_parameters )
