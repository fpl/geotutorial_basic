#!/usr/bin/python
    
import osgeo.ogr
import os.path
import sys

def analyzeGeometry(geometry, indent=0):
    s = []
    s.append("  " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")

    print "".join(s)

    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent+1)

mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
shapefile_name = os.path.join(mypath,"../files/tl_2012_us_cbsa.shp")
shapefile = osgeo.ogr.Open(shapefile_name)
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(55)
geometry = feature.GetGeometryRef()

analyzeGeometry(geometry)
