#!/usr/bin/python3

# Numpy/gdalnumeric - Read an image, extract a band, save a new image
from osgeo import gdalnumeric
srcArray = gdalnumeric.LoadFile("../files/SatImage.tif")
band1 = srcArray[0]
gdalnumeric.SaveArray(band1, "band1.jpg", format="JPEG")
