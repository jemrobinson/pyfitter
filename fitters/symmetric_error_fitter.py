from base_fitter import BaseFitter
from scipy.optimize import curve_fit

class SymmetricErrorFitter(BaseFitter) :
  '''Fit data with symmetric errors'''
  def __init__( self, x, y, ey, *args, **kwargs ) :
    super(SymmetricErrorFitter, self).__init__(*args,**kwargs)
    self.x = x
    self.y = y
    self.ey = ey

  def fit( self, function, initial_parameters ) :
    x, y, ey = zip( *( (x,y,ey) for x, y, ey in zip(self.x,self.y,self.ey) if ey != 0 ) )
    extracted_parameters, covariance_matrix = curve_fit( function, x, y, sigma=ey, p0=initial_parameters )
    return (extracted_parameters,covariance_matrix)
