#Examine a shapefile with ogr                                                                        

from osgeo import ogr
# open the shapefile
shp = ogr.Open("point.shp")
# Get the layer
layer = shp.GetLayer()
# Loop through the features
# and print information about them
for feature in layer:
  geometry = feature.GetGeometryRef()
  print geometry.GetX(), geometry.GetY(), feature.GetField("FIRST_FLD")
