#!/usr/bin/python

import osgeo.ogr
import os.path

import sys

def findPoints(geometry, results):
    for i in range(geometry.GetPointCount()):
        x,y,z = geometry.GetPoint(i)
        if results['north'] == None or results['north'][1] < y:
            results['north'] = (x,y)
        if results['south'] == None or results['south'][1] > y:
            results['south'] = (x,y)

    for i in range(geometry.GetGeometryCount()):
        findPoints(geometry.GetGeometryRef(i), results)

mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
shapefile_name = os.path.join(mypath,"../files/tl_2012_us_cbsa.shp")
shapefile = osgeo.ogr.Open(shapefile_name)
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(55)
geometry = feature.GetGeometryRef()

results = {'north' : None,
           'south' : None}

findPoints(geometry, results)

print "Northernmost point is (%0.4f, %0.4f)" % results['north']
print "Southernmost point is (%0.4f, %0.4f)" % results['south']
