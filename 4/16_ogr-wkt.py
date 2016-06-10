# Convert a shapefile to WKT using ogr
from osgeo import ogr
shape = ogr.Open("polygon.shp")
layer = shape.GetLayer()
feature = layer.GetNextFeature()
geom = feature.GetGeometryRef()
wkt = geom.ExportToWkt()
# View the WKT
print wkt
# Ingest the WKT we made and check the envelope
poly = ogr.CreateGeometryFromWkt(wkt)
print poly.GetEnvelope()
