#!/usr/bin/python

from osgeo import ogr
import os
import sys

# set the working directory
os.chdir('../files')
# get the driver
driver = ogr.GetDriverByName('ESRI Shapefile')
# open the data source
datasource = driver.Open('point.shp', 0)
if datasource is None:
    print 'Could not open file'
    sys.exit(1)
# get the data layer
layer = datasource.GetLayer()
# loop through the features and count them
cnt = 0
feature = layer.GetNextFeature()
while feature:
    cnt = cnt + 1
    feature.Destroy()
    feature = layer.GetNextFeature()
    print 'There are ' + str(cnt) + ' features'
# close the data source
datasource.Destroy()
