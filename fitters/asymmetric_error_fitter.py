from base_fitter import BaseFitter
from scipy.optimize import curve_fit

class AsymmetricErrorFitter(BaseFitter) :
  '''Fit data with asymmetric errors'''
  def __init__( self, *args,**kwargs ) :
    super(AsymmetricErrorFitter, self).__init__(*args,**kwargs)

  def fit( self, function, initial_parameters ) :
    print self.ey
    # x, y, ey = zip( *( (x,y,ey) for x, y, ey in zip(self.x,self.y,self.ey) if ey != 0 ) )
    extracted_parameters, covariance_matrix = curve_fit( function, x, y, sigma=ey, p0=initial_parameters )
    return (extracted_parameters,covariance_matrix)
