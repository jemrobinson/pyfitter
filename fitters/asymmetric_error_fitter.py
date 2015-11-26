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


  def __single_point_weighted_chi( self, x, y, ey_low, ey_high, function, parameters ) :
    '''Asymmetric chi^2 at a single data point'''
    fit = function(x,*parameters)
    if y > fit and ey_high != 0 : return abs( (y - fit) / ey_high )
    if y <= fit and ey_low != 0 : return abs( (y - fit) / ey_low )
    return 0


  def __total_chi_squared( self, function, parameters ) :
    '''Sum of asymmetric chi^2'''
    chi_squared = 0
    for _x, _y, _ey_low, _ey_high in zip(self.x,self.y,self.ey_low,self.ey_high) :
      chi_squared += self.__single_point_weighted_chi( _x, _y, _ey_low, _ey_high, function, parameters )**2
    return chi_squared


  def _update_chisq_ndof( self, function ) :
    '''Inherited from base class: update chi^2 and ndof'''
    self._chi_squared = self.__total_chi_squared( function, self.fit_parameters )
    self._ndof = len(self.x) - len(self.fit_parameters)


  def loss_function_summed( self, function ) :
    return partial( self.__total_chi_squared, function )


  def loss_function_vectorised( self, parameters, function ) :
    return [ self.__single_point_weighted_chi( x, y, ey_low, ey_high, function, parameters ) for x, y, ey_low, ey_high in zip(self.x, self.y, self.ey_low, self.ey_high) ]


  def _fit( self, function, initial_parameters, parameter_bounds=None ) :
    '''Inherited from base class: fit data with function'''
    # Run minimiser with bounds
    if parameter_bounds == None :
      fit_result = scipy.optimize.minimize( self.loss_function_summed( function ), initial_parameters, jac=False )
    else :
      fit_result = scipy.optimize.minimize( self.loss_function_summed( function ), initial_parameters, jac=False, bounds=parameter_bounds )
    # Run leastsq with best fit parameters as input to estimate covariance
    fit_result_lsq = scipy.optimize.leastsq( self.loss_function_vectorised, fit_result.x, args=(function), full_output=True )
    self._fit_parameters, self._covariance = fit_result_lsq[0], fit_result_lsq[1]
