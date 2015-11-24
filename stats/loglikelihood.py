from scipy.interpolate import interpolate
from scipy.stats import poisson
import math
import numpy as np

def error( values ) :
  try :
    errors = [ _error(value) for value in values ]
  except TypeError :
    errors = _error(values)
  return errors

def _error( value ) :
  '''Construct log likelihood errors using Poisson distribution'''
  # likelihood = P(value|lambda) using underlying Poisson assumption
  n_samples = 1000
  lambdas, loglikelihoods = zip( *( (x,-2*poisson.logpmf(value,x)) for x in np.linspace(1,2*value,n_samples) ) )
  interpolated_ll = interpolate.interp1d(lambdas, loglikelihoods)
  # up error: lambda for which interpolated_ll(lambda) = interpolated_ll(value) + 1
  # down error: lambda for which interpolated_ll(lambda) = interpolated_ll(value) + 1
  ll_at_value, lambda_up, lambda_down, step_size = interpolated_ll(value), value, value, float(value)/10
  for i in range(5) :
    lambda_up -= step_size; lambda_down += step_size; step_size /= 10
    while interpolated_ll(lambda_down) - ll_at_value < 1 : lambda_down -= step_size
    while interpolated_ll(lambda_up) - ll_at_value < 1 : lambda_up += step_size
  return (value-lambda_down,lambda_up-value)
