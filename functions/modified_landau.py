from base_function import BaseFunction
import math

class ModifiedLandau(BaseFunction) :
  def __init__( self, **kwargs ) :
    '''normalisation=1, mu=0, Gamma=1, width_scale=1'''
    super(ModifiedLandau, self).__init__(**kwargs)


  def _pdf( self, x, normalisation, mu, Gamma, width_scale ) :
    integral = self._integrate_unnormalised_pdf( parameters=(mu, Gamma, width_scale) )
    if integral != 0 : return normalisation * self._unnormalised_pdf( x, mu, Gamma, width_scale ) / integral
    return 0


  def _unnormalised_pdf( self, x, mu, Gamma, width_scale ) :
    width = Gamma + width_scale * x
    if width <= 0 : return 0
    lf = (x-mu)/width
    p1=(0.4259894875,-0.1249762550,0.03984243700,-0.006298287635,0.001511162253)
    q1=(1.0,-0.3388260629,0.09594393323,-0.01608042283,0.003778942063)
    p2=(0.1788541609,0.1173957403,0.01488850518,-0.001394989411,0.0001283617211)
    q2=(1.0,0.7428795082,0.3153932961,0.06694219548,0.008790609714)
    p3=(0.1788544503,0.09359161662,0.006325387654,0.00006611667319,-0.000002031049101)
    q3=(1.0,0.6097809921,0.2560616665,0.04746722384,0.006957301675)
    p4=(0.9874054407,118.6723273,849.2794360,-743.7792444,427.0262186)
    q4=(1.0,106.8615961,337.6496214,2016.712389,1597.063511)
    p5=(1.003675074,167.5702434,4789.711289,21217.86767,-22324.94910)
    q5=(1.0,156.9424537,3745.310488,9834.698876,66924.28357)
    p6=(1.000827619,664.9143136,62972.92665,475554.6998,-5743609.109)
    q6=(1.0,651.4101098,56974.73333,165917.4725,-2815759.939)
    a1=(0.04166666667,-0.01996527778,0.02709538966)
    a2=(-1.845568670,-4.284640743)
    if lf < -5.5 :
      u   = math.exp(lf+1.0)
      if u < 1e-10 : return 0.0
      ue  = math.exp(-1/u)
      us  = math.sqrt(u)
      output = 0.3989422803*(ue/us)*(1+(a1[0]+(a1[1]+a1[2]*u)*u)*u)
    elif lf < -1 :
      u   = math.exp(-lf-1)
      output = math.exp(-u)*math.sqrt(u)*(p1[0]+(p1[1]+(p1[2]+(p1[3]+p1[4]*lf)*lf)*lf)*lf)/(q1[0]+(q1[1]+(q1[2]+(q1[3]+q1[4]*lf)*lf)*lf)*lf)
    elif lf < 1 :
      output = (p2[0]+(p2[1]+(p2[2]+(p2[3]+p2[4]*lf)*lf)*lf)*lf)/(q2[0]+(q2[1]+(q2[2]+(q2[3]+q2[4]*lf)*lf)*lf)*lf)
    elif lf < 5 :
      output = (p3[0]+(p3[1]+(p3[2]+(p3[3]+p3[4]*lf)*lf)*lf)*lf)/(q3[0]+(q3[1]+(q3[2]+(q3[3]+q3[4]*lf)*lf)*lf)*lf)
    elif lf < 12 :
      u   = 1/lf
      output = u*u*(p4[0]+(p4[1]+(p4[2]+(p4[3]+p4[4]*u)*u)*u)*u)/(q4[0]+(q4[1]+(q4[2]+(q4[3]+q4[4]*u)*u)*u)*u)
    elif lf < 50 :
      u   = 1/lf
      output = u*u*(p5[0]+(p5[1]+(p5[2]+(p5[3]+p5[4]*u)*u)*u)*u)/(q5[0]+(q5[1]+(q5[2]+(q5[3]+q5[4]*u)*u)*u)*u)
    elif lf < 300 :
      u   = 1/lf
      output = u*u*(p6[0]+(p6[1]+(p6[2]+(p6[3]+p6[4]*u)*u)*u)*u)/(q6[0]+(q6[1]+(q6[2]+(q6[3]+q6[4]*u)*u)*u)*u)
    else :
      u   = 1/(lf-lf*math.log(lf)/(lf+1))
      output = u*u*(1+(a2[0]+a2[1]*u)*u)
    return output
