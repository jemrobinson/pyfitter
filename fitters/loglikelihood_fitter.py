from base_fitter import BaseFitter
import numpy as np
import scipy


class LogLikelihoodFitter(BaseFitter) :
  '''Fit data using maximum likelihood estimation'''
  def __init__( self, x, y, *args, **kwargs ) :
    super(LogLikelihoodFitter, self).__init__(*args,**kwargs)
    self.x = np.array( x )
    self.y = np.array( y )


  def _update_chisq_ndof( self ) :
    '''Inherited from base class: update chi^2 and ndof'''
    self._chi_squared = np.sum( np.square( self.y_predicted() - self.y ) / self.y_predicted() )
    self._ndof = len(self.x) - len(self.fit_parameters)


  def __negative_log_likelihood( self, parameters ) :
    if any( _fit_y == 0 for _fit_y in self.y_predicted(parameters) ) : return 1e99
    return np.sum(self.y_predicted(parameters)) - np.sum( np.array(self.y)*np.log(self.y_predicted(parameters)) )


  def __calculate_covariance( self ) :
    # Vinv_ij = np.zeros( shape=(self.fit_parameters.size,self.fit_parameters.size) )
    # for i in range(self.fit_parameters.size) :
    #   for j in range(self.fit_parameters.size) :
    #     parameters_up, parameters_dn = np.array(self.fit_parameters), np.array(self.fit_parameters)
    #     parameters_up[i] *= (1+1e-10); parameters_up[j] *= (1+1e-10)
    #     parameters_dn[i] *= (1-1e-10); parameters_dn[j] *= (1-1e-10)
    #     dsq_negative_LL = ( self.__negative_log_likelihood(parameters_up) - self.__negative_log_likelihood(parameters_dn) )**2
    #     d_theta_i = parameters_up[i] - parameters_dn[i]
    #     d_theta_j = parameters_up[j] - parameters_dn[j]
    #     Vinv_ij[i][j] = abs( dsq_negative_LL / (d_theta_i * d_theta_j) )
    # self._covariance = np.linalg.inv( Vinv_ij )
    self._covariance = np.zeros( shape=(self.fit_parameters.size,self.fit_parameters.size) )


  def _fit( self, initial_parameters, parameter_bounds=None ) :
    '''Inherited from base class: fit data with function'''
    # Run minimiser with bounds
    if parameter_bounds == None :
      fit_result = scipy.optimize.minimize( self.__negative_log_likelihood, initial_parameters, jac=False )
    else :
      fit_result = scipy.optimize.minimize( self.__negative_log_likelihood, initial_parameters, jac=False, bounds=parameter_bounds )
    self._fit_parameters = fit_result.x
    self.__calculate_covariance()
