import scipy

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct Poisson errors for known lambda'''
  # error: standard deviation -> sqrt(n)
  if value == 0 : return ( 0, 0 )
  return ( scipy.stats.poisson.std(value), scipy.stats.poisson.std(value) )
