def TH1_to_arrays( histogram, x_range=None, y_range=None ) :
  '''Returns (x_points,y_points,ey_points) for specified x_range'''
  x, y, ey = [], [], []
  if x_range is not None : assert( len(x_range) == 2 )
  if y_range is not None : assert( len(y_range) == 2 )
  for bin in range(histogram.GetNbinsX()+1) :
    _x, _y, _ey = histogram.GetBinCenter(bin), histogram.GetBinContent(bin), histogram.GetBinError(bin)
    if x_range is not None :
      if x_range[0] is not None and _x < x_range[0] : continue
      if x_range[1] is not None and _x > x_range[1] : continue
    if y_range is not None :
      if y_range[0] is not None and _y < y_range[0] : continue
      if y_range[1] is not None and _y > y_range[1] : continue
    x.append( _x )
    y.append( _y )
    ey.append( _ey )
  return [ x, y, ey ]
