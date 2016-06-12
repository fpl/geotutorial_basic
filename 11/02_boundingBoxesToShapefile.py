'''
Save countries bb in a new shapefile
'''
import os, os.path, shutil

from osgeo import ogr
from osgeo import osr

# Open the source shapefile.

srcFile = ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
srcLayer = srcFile.GetLayer(0)

# Open the output shapefile.

if os.path.exists("bounding-boxes"):
    shutil.rmtree("bounding-boxes")
os.mkdir("bounding-boxes")

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')

driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("bounding-boxes", "boundingBoxes.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer", spatialReference)

fieldDef = ogr.FieldDefn("NAME", ogr.OFTString)
fieldDef.SetWidth(50)
dstLayer.CreateField(fieldDef)

fieldDef = ogr.FieldDefn("ISO3", ogr.OFTString)
fieldDef.SetWidth(3)
dstLayer.CreateField(fieldDef)

# Read the country features from the source shapefile.

for i in range(srcLayer.GetFeatureCount()):
    feature = srcLayer.GetFeature(i)
    countryCode = feature.GetField("ISO3")
    countryName = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()
    minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()

    # Save the bounding box as a feature in the output
    # shapefile.

    linearRing = ogr.Geometry(ogr.wkbLinearRing)
    linearRing.AddPoint(minLong, minLat)
    linearRing.AddPoint(maxLong, minLat)
    linearRing.AddPoint(maxLong, maxLat)
    linearRing.AddPoint(minLong, maxLat)
    linearRing.AddPoint(minLong, minLat)

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(linearRing)

    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(polygon)
    feature.SetField("NAME", countryName)
    feature.SetField("ISO3", countryCode)
    dstLayer.CreateFeature(feature)
    feature.Destroy()

# All done.

srcFile.Destroy()
dstFile.Destroy()

