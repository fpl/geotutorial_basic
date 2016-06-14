# Examine a shapefile with pyshp                                                                                     import shapefile
import shapefile

shp = shapefile.Reader("point")
for feature in shp.shapeRecords():
  point = feature.shape.points[0]
  rec = feature.record[0]
  print point[0], point[1], rec
