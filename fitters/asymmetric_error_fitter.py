from base_fitter import BaseFitter
from functools import partial
import math
import numpy as np
import scipy


class AsymmetricErrorFitter(BaseFitter) :
  '''Fit data with asymmetric errors'''
  def __init__( self, x, y, ey_low, ey_high, *args, **kwargs ) :
    super(AsymmetricErrorFitter, self).__init__(*args,**kwargs)
    self.x = x
    self.y = y
    self.ey_low = ey_low
    self.ey_high = ey_high


  def __single_point_asymmetric_chi( self, x, y, ey_low, ey_high, parameters ) :
    '''Asymmetric chi at a single data point'''
    fit = self._function(x,*parameters)
    if y > fit and ey_high != 0 : return abs( (y - fit) / ey_high )
    if y <= fit and ey_low != 0 : return abs( (y - fit) / ey_low )
    return 0


  def __asymmetric_chi_squared_array( self, parameters, parameter_bounds=None ) :
    '''Array of chi^2 values for each point'''
    chi_squared_array = [ self.__single_point_asymmetric_chi( _x, _y, _ey_low, _ey_high, parameters )**2 for _x, _y, _ey_low, _ey_high in zip(self.x,self.y,self.ey_low,self.ey_high) ]
    # Return large value if out of bounds
    if parameter_bounds is not None :
      for parameter, bounds in zip( parameters, parameter_bounds ) :
        if (bounds[0] is not None and parameter < bounds[0]) or (bounds[1] is not None and parameter > bounds[1]) :
          chi_squared_array = [ 10 * _chi_squared for _chi_squared in chi_squared_array ]
    return chi_squared_array


  def __asymmetric_chi_squared_sum( self, parameters ) :
    '''Sum of asymmetric chi^2'''
    return np.sum( self.__asymmetric_chi_squared_array(parameters) )


  def _update_chisq_ndof( self ) :
    '''Inherited from base class: update chi^2 and ndof'''
    self._chi_squared = self.__asymmetric_chi_squared_sum(self.fit_parameters)
    self._ndof = len(self.x) - len(self.fit_parameters)


  def _fit( self, initial_parameters, parameter_bounds=None ) :
    '''Inherited from base class: fit data with function'''
    # Run minimiser with bounds
    if parameter_bounds == None :
      fit_result = scipy.optimize.minimize( self.__asymmetric_chi_squared_sum, initial_parameters, jac=False )
    else :
      fit_result = scipy.optimize.minimize( self.__asymmetric_chi_squared_sum, initial_parameters, jac=False, bounds=parameter_bounds )
    # Run leastsq with best fit parameters as input to estimate covariance
    fit_result_lsq = scipy.optimize.leastsq( self.__asymmetric_chi_squared_array, fit_result.x, args=(parameter_bounds), full_output=True )
    self._fit_parameters, self._covariance = fit_result_lsq[0], fit_result_lsq[1]
