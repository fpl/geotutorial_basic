import osgeo.ogr
import os.path
import sys

mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
shapefile_name = os.path.join(mypath,"../files/tl_2012_us_state.shp")
shapefile = osgeo.ogr.Open(shapefile_name)
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)

print "Feature 2 has the following attributes:"
print

attributes = feature.items()

for key,value in attributes.items():
    print " %s = %s" % (key, value)

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()

print
print "Feature's geometry data consists of a %s" % geometryName
