from base_function import BaseFunction
import math
import numpy as np

class Exponential(BaseFunction) :
  def __init__( self, **kwargs ) :
    '''Parameters are normalisation and decay_constant'''
    super(Exponential, self).__init__( default_x_range=(0,1e3), **kwargs )


  def _pdf( self, x, normalisation, decay_constant ) :
    integral = self._integrate_unnormalised_pdf( parameters=(decay_constant) )
    if integral != 0 : return normalisation * self._unnormalised_pdf( x, decay_constant ) / integral
    return 0


  def _unnormalised_pdf( self, x, decay_constant ) :
    return decay_constant * math.exp( -decay_constant * x )
