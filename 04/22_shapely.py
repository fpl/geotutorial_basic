#!/usr/bin/python3

# Create a polygon buffer with shapely

from shapely import wkt, geometry
# Create a simple wkt polygon string
wktPoly = "POLYGON((0 0,4 0,4 4,0 4,0 0))"
# Load the polygon into shapely
poly = wkt.loads(wktPoly)
# Check the area
print(poly.area)
# Create a buffer
buf =(poly.buffer(5.0)
# Get the buffer area
print(buf.area)
# Compute the difference between the two
print(buf.difference(poly).area)

