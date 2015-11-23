from base_fitter import BaseFitter
import scipy

class SymmetricErrorFitter(BaseFitter) :
  '''Fit data with symmetric errors'''
  def __init__( self, *args,**kwargs ) :
    super(SymmetricErrorFitter, self).__init__(*args,**kwargs)

  def fit( self, function ) :
    extracted_parameters, covariance_matrix = scipy.optimize.curve_fit( function, self.x, self.y, sigma=self.ey, p0=self.initial_parameters )
    return (extracted_parameters,covariance_matrix)
