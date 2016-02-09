from base_function import BaseFunction
import math

class DoubleSidedCrystalBall(BaseFunction) :
  def __init__( self, **kwargs ) :
    ''', normalisation=1, mu=1, sigma=1, alpha_low=1, alpha_high=1, n_low=1, n_high=1'''
    super(DoubleSidedCrystalBall, self).__init__(**kwargs)


  def _pdf( self, x, normalisation, mu, sigma, alpha_low, alpha_high, n_low, n_high ) :
    integral = self._integrate_unnormalised_pdf( parameters=(mu, sigma, alpha_low, alpha_high, n_low, n_high) )
    if integral != 0 : return normalisation * self._unnormalised_pdf( x, mu, sigma, alpha_low, alpha_high, n_low, n_high ) / integral
    return 0


  def _unnormalised_pdf( self, x, mu, sigma, alpha_low, alpha_high, n_low, n_high ) :
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
      return output
    except ValueError :
      return 0
