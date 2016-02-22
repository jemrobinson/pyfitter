import numpy as np

class BaseFitter(object) :
  '''Fit data with errors'''
  def __init__( self ) :
    self._fit_parameters = []
    self._function = None
    self._covariance = []
    self._fit_errors = []
    self._chi_squared = 0
    self._ndof = 0


  def fit( self, function, initial_parameters=None, *args, **kwargs ) :
    self._function = function
    self._fit( initial_parameters, *args, **kwargs )
    self._update_chisq_ndof()
    if self.covariance is not None :
      self._fit_errors = np.sqrt(np.diag(self.covariance)) #[ np.sqrt(self.covariance[idx][idx]) for idx in range(len(self.covariance)) ]


  def _fit( self, initial_parameters, *args, **kwargs ) :
    raise NotImplementedError('Must be implemented by child classes')


  def _update_chisq_ndof( self ) :
    raise NotImplementedError('Must be implemented by child classes')


  def y_predicted( self, parameters=None ) :
    if parameters is None : parameters = self._fit_parameters
    return np.array( [ self._function(_x,*parameters) for _x in self.x ] )


  @property
  def fit_errors(self) :
    return self._fit_errors

  @property
  def fit_parameters(self) :
    return self._fit_parameters

  @property
  def covariance(self) :
    return self._covariance

  @property
  def chi_squared(self) :
    return self._chi_squared

  @property
  def ndof(self):
    return self._ndof
