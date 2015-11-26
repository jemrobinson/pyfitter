import numpy as np
from scipy.interpolate import interpolate

class BaseFunction(object) :
  '''Function which can be evaluated at a point or operate on an array'''
  def __init__( self ) :
    self.inv_cdf = None
    self.interpolation_range = None


  def at( self, value, **kwargs ) :
    raise NotImplementedError('Should be implemented by child class')


  def vectorised( self ) :
    return np.vectorize( self.at )


  def inverse_trf(self):
    if self.inv_cdf is None :
      n_bins, n_samples = 10000, 10000
      x = np.linspace( self.interpolation_range[0], self.interpolation_range[1], n_samples )
      y = self.vectorised()(x)
      hist, bin_edges = np.histogram( x, bins=n_bins, weights=y, normed=True )
      cum_values = np.zeros(bin_edges.shape)
      cum_values[1:] = np.cumsum(hist*np.diff(bin_edges))
      self.inv_cdf = interpolate.interp1d(cum_values, bin_edges, kind='linear')
    return self.inv_cdf


  def sample_from( self, n ) :
    return [ self.inverse_trf()(r) for r in np.random.rand(n) ]
