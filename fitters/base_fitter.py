class BaseFitter(object) :
  '''Fit data with errors'''
  def __init__( self, x, y, ey=None, function=None ) :
    self.x = x
    self.y = y
    self.ey = ey
    self.function = function
    # self.initial_parameters = initial_parameters

  def fit( self, *args ) :
    raise NotImplementedError('Should be implemented by child class')






  # extracted_parameters, pcov = curve_fit( vec_func_Landau, x, y, sigma=ey, p0=[300, 30, 100] )
  #
  # def fit_function( self, **kwargs ) :
  #   return np.vectorize( self.evaluate(**kwargs) )
