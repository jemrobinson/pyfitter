pyfitter
========

Data fitting with python.


Inputs
======
Lists of x, y and errors on y. Can be obtained from ROOT input using ```pyfitter.interpreters```


Outputs
=======
Lists of parameter values from fit results



Example: fitting a Landau to data
=================================
Construct a dataset by sampling
```python
input_landau = pyfitter.functions.Landau(mpv=5,sigma=1.5)
h_data = ROOT.TH1D( 'h_data', 'Pseudo-data sampled from Landau', 100, 0.0, 20.0 )
[ h_data.Fill( x ) for x in input_landau.sample_from(1000) ]
```

Fit with symmetric (naive Poisson) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
symmetric_fitter = pyfitter.fitters.SymmetricErrorFitter( x, y, ey )
symmetric_fitter.fit( pyfitter.functions.Landau().vectorised(), initial_parameters=[2, 1, 100] )
print 'Parameters:',symmetric_fitter.parameters
print 'Covariance:',symmetric_fitter.covariance
```

Fit with asymmetric (frequentist) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
ey_l, ey_h = zip( *( pyfitter.stats.frequentist.error(_y) for _y in y ) )
asymmetric_fitter = pyfitter.fitters.AsymmetricErrorFitter( x, y, ey_l, ey_h )
asymmetric_fitter.fit( pyfitter.functions.Landau().vectorised(), initial_parameters=[2, 1, 100], parameter_bounds=[(None,None),(0,None),(0,None)] )
print 'Parameters:',asymmetric_fitter.parameters
print 'Covariance:',asymmetric_fitter.covariance
```
