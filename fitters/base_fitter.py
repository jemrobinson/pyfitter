class BaseFitter(object) :
  '''Fit data with errors'''
  def __init__( self ) :
    pass

  def fit( self, *args ) :
    raise NotImplementedError('Should be implemented by child class')






  # extracted_parameters, pcov = curve_fit( vec_func_Landau, x, y, sigma=ey, p0=[300, 30, 100] )
  #
  # def fit_function( self, **kwargs ) :
  #   return np.vectorize( self.evaluate(**kwargs) )
