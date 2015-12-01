def TH1_to_arrays( histogram, x_ranges=[], y_ranges=[] ) :
  '''Returns (x_points,y_points,ey_points) for specified x and y ranges'''
  x, y, ey = [], [], []
  for x_range in x_ranges : assert( len(x_range) == 2 )
  for y_range in y_ranges : assert( len(y_range) == 2 )
  for bin in range(histogram.GetNbinsX()+1) :
    _x, _y, _ey, _skip_bin = histogram.GetBinCenter(bin), histogram.GetBinContent(bin), histogram.GetBinError(bin), False
    for x_range in x_ranges :
      if x_range[0] is not None and _x <= x_range[0] : _skip_bin = True
      if x_range[1] is not None and _x > x_range[1] : _skip_bin = True
    for y_range in y_ranges :
      if y_range[0] is not None and _y <= y_range[0] : _skip_bin = True
      if y_range[1] is not None and _y > y_range[1] : _skip_bin = True
    if _skip_bin : continue
    x.append( _x )
    y.append( _y )
    ey.append( _ey )
  return [ x, y, ey ]
