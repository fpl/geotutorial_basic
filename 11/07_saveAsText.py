# saveAsText.py

import os,os.path,shutil

from osgeo import ogr

if os.path.exists("country-wkt-files"):
    shutil.rmtree("country-wkt-files")
os.mkdir("country-wkt-files")

shapefile = ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
layer = shapefile.GetLayer(0)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    name = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()

    f = file(os.path.join("country-wkt-files",
                          name + ".txt"), "w")
    f.write(geometry.ExportToWkt())
    f.close()
