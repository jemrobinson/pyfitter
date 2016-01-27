from base_function import BaseFunction
import math

class DoubleSidedCrystalBall(BaseFunction) :
  def __init__( self, normalisation=1, mu=1, sigma=1, alpha_low=1, alpha_high=1, n_low=1, n_high=1 ) :
    super(DoubleSidedCrystalBall, self).__init__()
    self.normalisation = normalisation
    self.mu = mu
    self.sigma = sigma
    self.alpha_low = alpha_low
    self.alpha_high = alpha_high
    self.n_low = n_low
    self.n_high = n_high
    # self.interpolation_range = ( decay_constant*1e-10, decay_constant*10 )


  def pdf( self, x, normalisation=None, mu=None, sigma=None, alpha_low=None, alpha_high=None, n_low=None, n_high=None ) :
    if normalisation is None : normalisation = self.normalisation
    if mu is None : mu = self.mu
    if sigma is None : sigma = self.sigma
    if alpha_low is None : alpha_low = self.alpha_low
    if alpha_high is None : alpha_high = self.alpha_high
    if n_low is None : n_low = self.n_low
    if n_high is None : n_high = self.n_high
    if sigma == 0 : return 0
    try :
      x_norm = ( (x - mu) / sigma )
      if (x_norm < -alpha_low ) :
        A = math.exp(-0.5*alpha_low*alpha_low)
        B = n_low/math.fabs(alpha_low) - math.fabs(alpha_low)
        output = A * math.pow( math.fabs(alpha_low)/n_low * (B - x_norm), -n_low )
      elif (x_norm > alpha_high) :
        A = math.exp(-0.5*alpha_high*alpha_high)
        B = n_high/alpha_high - alpha_high
        output = A * math.pow( math.fabs(alpha_high)/n_high * (B + x_norm), -n_high )
      else :
        output = math.exp(-0.5*x_norm*x_norm)
      return normalisation * output
    except ValueError :
      return 0

    # try :
    #   A = math.pow( float(n)/math.fabs(alpha), n ) * math.exp( -(math.pow(alpha,2)/2) )
    #   B = ( float(n)/math.fabs(alpha) ) - math.fabs(alpha)
    #   C = ( float(n)/math.fabs(alpha) ) * math.exp( - (math.fabs(alpha)**2/2) ) / (n-1)
    #   D = math.sqrt( math.pi / 2 ) * ( 1 + math.erf( math.fabs(alpha) / math.sqrt(2) ) )
    #   N = 1. / ( sigma*(C+D) )
    #   x_norm = ( (x - mu) / sigma )
    #   if x_norm <= -alpha : output = N * A * math.pow( (B - x_norm), -n )
    #   if x_norm >= alpha : output = N * A * math.pow( (B + x_norm), -n )
    #   else : output = N * math.exp( -0.5*math.pow(x_norm,2) )
    #   return normalisation * output
    # except ValueError :
    #   return float('NaN')
