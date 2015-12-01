# from ..functions import BaseFunction
# import numpy as np

class BaseFitter(object) :
  '''Fit data with errors'''
  def __init__( self ) :
    self._fit_parameters = []
    self._covariance = []
    self._chi_squared = 0
    self._ndof = 0


  def fit( self, function, initial_parameters=None, *args, **kwargs ) :
    # _function = function
    # if isinstance( _function, BaseFunction ) : _function = np.vectorize( function )
    # self._fit( _function, initial_parameters, *args, **kwargs )
    self._fit( function, initial_parameters, *args, **kwargs )
    self._update_chisq_ndof( function )


  def _fit( self, function, initial_parameters, *args, **kwargs ) :
    raise NotImplementedError('Must be implemented by child classes')


  def _update_chisq_ndof( self, function ) :
    raise NotImplementedError('Must be implemented by child classes')


  @property
  def fit_parameters(self):
    return self._fit_parameters

  @property
  def covariance(self):
    return self._covariance

  @property
  def chi_squared(self):
    return self._chi_squared

  @property
  def ndof(self):
    return self._ndof
