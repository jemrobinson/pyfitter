import functools
import numpy as np
import scipy
# from scipy.interpolate import interpolate
# import inspect

class BaseFunction(object) :
  '''Function which can be evaluated at a point or operate on an array'''
  def __init__( self, default_x_range=(-np.inf,np.inf), **kwargs ) :
    self.parameter_dict = {}
    self.x_ranges = kwargs.pop( "x_ranges", [default_x_range] )
    for attr in kwargs : self.parameter_dict[attr] = kwargs[attr]
    self.inv_cdf = None


  def __call__( self, *args, **kwargs ) :
    if isinstance( args[0], (int,float) ) : return self.pdf( *args, **kwargs )
    return np.vectorize( self.pdf )( *args, **kwargs )


  def integral( self, **kwargs ) :
    partial_fn = functools.partial( self.pdf, **kwargs )
    return sum( [ scipy.integrate.quad( partial_fn, x_range[0], x_range[1] )[0] for x_range in self.x_ranges ] )


  def _integrate_unnormalised_pdf( self, parameters ) :
    return sum( [ scipy.integrate.quad( self._unnormalised_pdf, x_range[0], x_range[1], args=parameters )[0] for x_range in self.x_ranges ] )


  def pdf( self, *args, **kwargs ) :
    if self.parameter_dict :
      arg_list = list(args)
      combined_kwargs = dict( kwargs.items() + self.parameter_dict.items() )
      for argname in self._pdf.__code__.co_varnames[:self._pdf.func_code.co_argcount][1:] :
        if argname not in combined_kwargs : combined_kwargs[argname] = arg_list.pop(0)
      return self._pdf( **combined_kwargs )
    else :
      return self._pdf( *args, **kwargs )


  def inverse_trf(self):
    if self.inv_cdf is None :
      n_bins, n_samples = 10000, 10000
      x = np.linspace( self.x_range[0], self.x_range[1], n_samples )
      y = np.vectorize( self )(x)
      hist, bin_edges = np.histogram( x, bins=n_bins, weights=y, normed=True )
      cum_values = np.zeros(bin_edges.shape)
      cum_values[1:] = np.cumsum(hist*np.diff(bin_edges))
      self.inv_cdf = scipy.interpolate.interpolate.interp1d(cum_values, bin_edges, kind='linear')
    return self.inv_cdf


  def sample_from( self, n ) :
    return [ self.inverse_trf()(r) for r in np.random.rand(n) ]
