#!/usr/bin/python3

# Read and write GeoJson using the geojson module 
import geojson
p = geojson.Point([-92, 37])
geojs = geojson.dumps(p)
print(geojs)
# Use __geo_interface__ between geojson and shapely
from shapely.geometry import asShape
point = asShape(p)
print(point.wkt)
