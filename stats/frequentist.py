from scipy.stats import poisson

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct frequentist errors using Poisson distribution'''
  # up error: smallest lambda for which P(n<=nobs|lambda) < (1-0.68268...)/2 = 0.15865...
  # down error: largest lambda for which P(n>=nobs|lambda) < (1-0.68268...)/2 = 0.15865...
  lambda_up, lambda_down, step_size = 1.1*value, 0.9*value, float(value)/10
  if value == 0 : return (0,1.8410216450100005) # save time with precomputed value
  if value < 1 : lambda_up, lambda_down, step_size =  1.8, 0.0, 0.1
  for i in range(5) :
    lambda_up -= step_size; lambda_down += step_size; step_size /= 10
    while poisson.cdf( value, lambda_up ) > 0.15865525393145705 : lambda_up += step_size
    while poisson.sf( value-1, lambda_down ) > 0.15865525393145705 : lambda_down -= step_size
  return (value-lambda_down,lambda_up-value)
