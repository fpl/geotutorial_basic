#!/usr/bin/python3

# Open a raster with gal
from osgeo import gdal
raster = gdal.Open("../files/SatImage.tif")
print(raster.RasterCount)
print(raster.RasterXSize)
print(raster.RasterYSize)
