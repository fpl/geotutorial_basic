# Open a raster with gal
from osgeo import gdal
raster = gdal.Open("SatImage.tif")
print raster.RasterCount
print raster.RasterXSize
print raster.RasterYSize
