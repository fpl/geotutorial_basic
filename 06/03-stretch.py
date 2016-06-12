"""Perform a histogram stretch on an image"""
import gdalnumeric
import operator

def histogram(a, bins=range(0,256)):
  """
  Histogram function for multi-dimensional array.
  a = array
  bins = range of numbers to match 
  """
  fa = a.flat
  n = gdalnumeric.numpy.searchsorted(gdalnumeric.numpy.sort(fa), bins)
  n = gdalnumeric.numpy.concatenate([n, [len(fa)]])
  hist = n[1:]-n[:-1] 
  return hist

def stretch(a):
  """
  Performs a histogram stretch on a gdalnumeric array image.
  """
  hist = histogram(a)
  lut = []
  for b in range(0, len(hist), 256):
    # step size
    step = reduce(operator.add, hist[b:b+256]) / 255
    # create equalization lookup table
    n = 0
    for i in range(256):
      lut.append(n / step)
      n = n + hist[i+b]
  gdalnumeric.numpy.take(lut, a, out=a)
  return a

src = "swap.tif"
arr = gdalnumeric.LoadFile(src)
stretched = stretch(arr)
gdalnumeric.SaveArray(arr, "stretched.tif", format="GTiff", prototype=src)
