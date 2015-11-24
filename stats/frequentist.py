from scipy.stats import poisson

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct frequentist errors using Poisson distribution'''
  # up error: smallest lambda for which P(n<=nobs|lambda) < (1-0.682689492137085897170465091264075844955825933453208781974788)/2 = 158655253931457051414767454367962077522087033273395609012605
  # down error: largest lambda for which P(n>=nobs|lambda) < (1-0.682689492137085897170465091264075844955825933453208781974788)/2 = 158655253931457051414767454367962077522087033273395609012605
  lambda_up, lambda_down, step_size = value, value, float(value)/10
  if value == 0 : lambda_up, lambda_down, step_size = 1e-10, 0, 1e-3
  for i in range(5) :
    lambda_up -= step_size; lambda_down += step_size; step_size /= 10
    while poisson.cdf( value, lambda_up ) > 0.15865525393145705 : lambda_up += step_size
    while poisson.sf( value-1, lambda_down ) > 0.15865525393145705 : lambda_down -= step_size
  return (value-lambda_down,lambda_up-value)
