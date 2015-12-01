pyfitter
========

Data fitting with python.


Inputs
======
Lists of x, y and errors on y. Can be obtained from ROOT input using ```pyfitter.interpreters```


Outputs
=======
Fit objects know about the
* parameter values from fit results
* covariance matrix of parameters
* chi^2 of fit
* number of degrees of freedom in fit


Example: fitting a Landau to data
=================================
Construct a dataset by sampling
```python
input_landau = pyfitter.functions.Landau(mpv=5,sigma=1.5)
ROOT.TH1.SetDefaultSumw2()
h_data = ROOT.TH1D( 'h_data', 'Pseudo-data sampled from Landau', 100, 0.0, 20.0 )
[ h_data.Fill( x ) for x in input_landau.sample_from(1000) ]
```

Fit with symmetric (naive Poisson) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
symmetric_fitter = pyfitter.fitters.SymmetricErrorFitter( x, y, ey )
symmetric_fitter.fit( pyfitter.functions.Landau(), initial_parameters=[2, 1, 100] )
print 'Parameters:',symmetric_fitter.parameters
print 'Covariance:',symmetric_fitter.covariance
```

Fit with asymmetric (frequentist) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
ey_l, ey_h = zip( *( pyfitter.stats.frequentist.error(_y) for _y in y ) )
asymmetric_fitter = pyfitter.fitters.AsymmetricErrorFitter( x, y, ey_l, ey_h )
asymmetric_fitter.fit( pyfitter.functions.Landau(), initial_parameters=[2, 1, 100], parameter_bounds=[(None,None),(0,None),(0,None)] )
print 'Parameters:',asymmetric_fitter.parameters
print 'Covariance:',asymmetric_fitter.covariance
```

Available functions
===================
Any user-defined function which has been vectorised with numpy.vectorize(). For convenience, pyfitter implements
* Landau


Available error calculators
===========================
Errors on (integer valued) data can be provided by
* known_poisson: naive sqrt(n) from a Poisson distribution with a known mean
* frequentist: 68% region given by P(n>=nobs|value_down) = P(n<=nobs|value_up)= 0.159
* log-likelihood ratio: Delta L = +/- 1
* Bayesian: 68% region satisfying P(value_down|nobs) = P(value_up|nobs);
