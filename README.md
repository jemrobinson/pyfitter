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
f_landau = pyfitter.functions.Landau(mpv=5,sigma=1.5)
[ h_data.Fill( x ) for x in f_landau.sample_from(1000) ]
```

Fit with symmetric (naive Poisson) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
fitter = pyfitter.fitters.SymmetricErrorFitter( x, y, ey )
symmetric_params, cov = fitter.fit( f_landau.vectorised(), initial_parameters=[2, 1, 100] )
print symmetric_params
f_symmetric_fit = pyfitter.functions.Landau(*symmetric_params) # output values
```

Fit with asymmetric (frequentist) errors
```python
x, y, ey = pyfitter.interpreters.TH1_to_arrays( h_data )
ey_l, ey_h = zip( *( pyfitter.stats.frequentist.error(_y) for _y in y ) )
fitter = pyfitter.fitters.AsymmetricErrorFitter( x, y, ey_l, ey_h )
asymmetric_params, cov = fitter.fit( f_landau.vectorised(), initial_parameters=[2, 1, 100], parameter_bounds=[(None,None),(0,None),(0,None)] )
print asymmetric_params
f_asymmetric_fit = pyfitter.functions.Landau(*asymmetric_params) # output values
```
