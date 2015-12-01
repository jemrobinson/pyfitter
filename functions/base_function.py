import numpy as np
from scipy.interpolate import interpolate

class BaseFunction(object) :
  '''Function which can be evaluated at a point or operate on an array'''
  def __init__( self ) :
    self.inv_cdf = None
    self.interpolation_range = None


  def __call__( self, *args, **kwargs ) :
    if isinstance( args[0], (int,float) ) : return self._call_function( *args, **kwargs )
    return np.vectorize( self._call_function )( *args, **kwargs )


  def _call_function( self, *args, **kwargs ) :
    raise NotImplementedError('Should be implemented by child class')


  def inverse_trf(self):
    if self.inv_cdf is None :
      n_bins, n_samples = 10000, 10000
      x = np.linspace( self.interpolation_range[0], self.interpolation_range[1], n_samples )
      y = np.vectorize( self )(x)
      hist, bin_edges = np.histogram( x, bins=n_bins, weights=y, normed=True )
      cum_values = np.zeros(bin_edges.shape)
      cum_values[1:] = np.cumsum(hist*np.diff(bin_edges))
      self.inv_cdf = interpolate.interp1d(cum_values, bin_edges, kind='linear')
    return self.inv_cdf


  def sample_from( self, n ) :
    return [ self.inverse_trf()(r) for r in np.random.rand(n) ]
