from scipy.stats import poisson

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct frequentist errors using Poisson distribution'''
  # up error: smallest lambda for which P(n<=nobs|lambda) < (1-0.682689492137085897170465091264075844955825933453208781974788)/2
  # down error: largest lambda for which P(n>=nobs|lambda) < (1-0.682689492137085897170465091264075844955825933453208781974788)/2
  if value == 0 :
    error_up, error_down, step_size = 1e-10, 0, 1e-3
  else :
    error_up, error_down, step_size = value, value, float(value)/10
  for i in range(3) :
    while poisson.cdf( value, error_up ) > 0.158655253931457051414767454367962077522087033273395609012605 : error_up += step_size
    while poisson.sf( value-1, error_down ) > 0.158655253931457051414767454367962077522087033273395609012605 : error_down -= step_size
    error_up -= step_size
    error_down += step_size
    step_size /= 10
  return (value-error_down,error_up-value)
