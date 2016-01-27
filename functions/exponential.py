from base_function import BaseFunction
import math

class exponential(BaseFunction) :
  def __init__( self, normalisation=1, decay_constant=1, offset=1 ) :
    super(exponential, self).__init__()
    self.normalisation = normalisation
    self.decay_constant = decay_constant
    self.offset = offset
    self.interpolation_range = ( decay_constant*1e-10, decay_constant*10 )


  def pdf( self, x, normalisation=None, decay_constant=None, offset=None ) :
    if normalisation is None : normalisation = self.normalisation
    if decay_constant is None : decay_constant = self.decay_constant
    if offset is None : offset = self.offset
    return normalisation * math.exp( -decay_constant * x) + offset
