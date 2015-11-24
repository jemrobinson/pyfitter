from scipy.stats import poisson

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct Poisson errors for known lambda'''
  # error: standard deviation -> sqrt(n)
  return ( poisson.std(value), poisson.std(value) )
