from osgeo import ogr
import os
import sys

driver = ogr.GetDriverByName('ESRI Shapefile')
# open the input data source and get the layer
inDS = driver.Open('polygon.shp', 0)
if inDS is None:
    print 'Could not open file'
    sys.exit(1)

inLayer = inDS.GetLayer()
# create a new data source and layer
if os.path.exists('test.shp'):
driver.DeleteDataSource('test.shp')
outDS = driver.CreateDataSource('test.shp')
if outDS is None:
    print 'Could not create file'
    sys.exit(1)
outLayer = outDS.CreateLayer('test', geom_type=ogr.wkbPoint)
# use the input FieldDefn to add a field to the output
fieldDefn = inLayer.GetFeature(0).GetFieldDefnRef('id')
outLayer.CreateField(fieldDefn)
# get the FeatureDefn for the output layer
featureDefn = outLayer.GetLayerDefn()
# loop through the input features
cnt = 0
inFeature = inLayer.GetNextFeature()
while inFeature:
	# create a new feature
	outFeature = ogr.Feature(featureDefn)
	outFeature.SetGeometry(inFeature.GetGeometryRef())
	outFeature.SetField('id', inFeature.GetField('id'))
	# add the feature to the output layer
	outLayer.CreateFeature(outFeature)
	# destroy the features
	inFeature.Destroy()
	outFeature.Destroy()
	# increment cnt and if we have to do more then keep looping
	cnt = cnt + 1
	if cnt < 10: inFeature = inLayer.GetNextFeature()
	else: break
# close the data sources
inDS.Destroy()
outDS.Destroy()
