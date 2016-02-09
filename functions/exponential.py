from base_function import BaseFunction
import math

class Exponential(BaseFunction) :
  def __init__( self, **kwargs ) :
    ''', normalisation=1, decay_constant=1, offset='''
    super(Exponential, self).__init__(**kwargs)


  def _pdf( self, x, normalisation, decay_constant, offset ) :
    integral = self._integrate_unnormalised_pdf( parameters=(decay_constant, offset) )
    if integral != 0 : return normalisation * self._unnormalised_pdf( x, decay_constant, offset ) / integral
    return 0


  def _unnormalised_pdf( self, x, decay_constant, offset ) :
    return math.exp( -decay_constant * x) + offset
