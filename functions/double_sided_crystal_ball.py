from base_function import BaseFunction
import math

class exponential(BaseFunction) :
  def __init__( self, normalisation=1, decay_constant=1, offset=1 ) :
    super(exponential, self).__init__()
    self.normalisation = normalisation
    self.decay_constant = decay_constant
    self.offset = offset
    self.interpolation_range = ( decay_constant*1e-10, decay_constant*10 )


  def pdf( self, x, normalisation=None, decay_constant=None, offset=None ) :
    if normalisation is None : normalisation = self.normalisation
    if decay_constant is None : decay_constant = self.decay_constant
    if offset is None : offset = self.offset
    return normalisation * math.exp( -decay_constant * x) + offset

# double fnc_dscb(double*xx,double*pp)
# {
#   double x   = xx[0];
#   // gaussian core
#   double N   = pp[0];//norm
#   double mu  = pp[1];//mean
#   double sig = pp[2];//variance
#   // transition parameters
#   double a1  = pp[3];
#   double p1  = pp[4];
#   double a2  = pp[5];
#   double p2  = pp[6];
#
#   double u   = (x-mu)/sig;
#   double A1  = TMath::Power(p1/TMath::Abs(a1),p1)*TMath::Exp(-a1*a1/2);
#   double A2  = TMath::Power(p2/TMath::Abs(a2),p2)*TMath::Exp(-a2*a2/2);
#   double B1  = p1/TMath::Abs(a1) - TMath::Abs(a1);
#   double B2  = p2/TMath::Abs(a2) - TMath::Abs(a2);
#
#   double result(N);
#   if      (u<-a1) result *= A1*TMath::Power(B1-u,-p1);
#   else if (u<a2)  result *= TMath::Exp(-u*u/2);
#   else            result *= A2*TMath::Power(B2+u,-p2);
#   return result;
# }
