def TH1_to_arrays( histogram, x_ranges=[], y_ranges=[] ) :
  '''Returns (x_points,y_points,ey_points) for specified x and y ranges'''
  x, y, ey = [], [], []
  for x_range in x_ranges : assert( len(x_range) == 2 )
  for y_range in y_ranges : assert( len(y_range) == 2 )
  for bin in range(histogram.GetNbinsX()+1) :
    _x, _y, _ey = histogram.GetBinCenter(bin), histogram.GetBinContent(bin), histogram.GetBinError(bin)
    _outside_x_ranges = len(x_ranges) > 0 and all( (x_range[0] is not None and _x < x_range[0]) or (x_range[1] is not None and _x > x_range[1]) for x_range in x_ranges )
    _outside_y_ranges = len(y_ranges) > 0 and all( (y_range[0] is not None and _y < y_range[0]) or (y_range[1] is not None and _y > y_range[1]) for y_range in y_ranges )
    if _outside_x_ranges or _outside_y_ranges : continue
    x.append( _x )
    y.append( _y )
    ey.append( _ey )
  return [ x, y, ey ]
