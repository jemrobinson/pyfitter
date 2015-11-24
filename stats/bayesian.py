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
  '''Construct Bayesian errors using Poisson distribution'''
  # likelihood = P(value|lambda) using underlying Poisson assumption
  # error: lambdas with equal likelihood for which area in between is 68%
  lambda_up, lambda_down, step_size = 1.1*value, 0.9*value, float(value)/10
  for i in range(5) :
    lambda_up -= step_size; lambda_down += step_size; step_size /= 10
    while (poisson.cdf(value,lambda_down) - poisson.cdf(value,lambda_up)) < 0.6826894921370859 :
      lambda_up += step_size
      while poisson.pmf(value,lambda_down) > poisson.pmf(value,lambda_up) : lambda_down -= step_size/10
  return (value-lambda_down,lambda_up-value)
