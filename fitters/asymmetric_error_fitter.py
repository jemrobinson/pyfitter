from base_fitter import BaseFitter
from scipy.optimize import curve_fit, minimize
from symmetric_error_fitter import SymmetricErrorFitter
from functools import partial

class AsymmetricErrorFitter(BaseFitter) :
  '''Fit data with asymmetric errors'''
  def __init__( self, x, y, ey_low, ey_high, *args, **kwargs ) :
    super(AsymmetricErrorFitter, self).__init__(*args,**kwargs)
    self.x = x
    self.y = y
    self.ey_low = ey_low
    self.ey_high = ey_high


  def __asymmetric_chi_squared( self, x, y, ey_low, ey_high, function, parameters ) :
    chi_squared = 0
    for _x, _y, _ey_low, _ey_high in zip(x,y,ey_low,ey_high) :
      fit = function(_x,*parameters)
      if _y > fit and _ey_high != 0 : chi_squared += ( (_y - function(_x,*parameters))/_ey_high )**2
      if _y <= fit and _ey_low != 0 : chi_squared += ( (_y - function(_x,*parameters))/_ey_low )**2
    # print parameters,'->',chi_squared
    return chi_squared


  def loss_function( self, x, y, ey_low, ey_high, function ) :
    bound_asymmetric_chi_squared = partial( self.__asymmetric_chi_squared, x, y, ey_low, ey_high, function )
    return bound_asymmetric_chi_squared


  def fit( self, function, initial_parameters, parameter_bounds=None ) :
    if parameter_bounds == None :
      fit_result = minimize( self.loss_function( self.x, self.y, self.ey_low, self.ey_high, function ), initial_parameters )
    else :
      fit_result = minimize( self.loss_function( self.x, self.y, self.ey_low, self.ey_high, function ), initial_parameters, bounds=parameter_bounds )
    if fit_result.success != True :
      print 'Fit was not successful!'
    return (fit_result.x,None)
