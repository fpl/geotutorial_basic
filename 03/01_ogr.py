import osgeo.ogr
import os.path
import sys

mypath = os.path.dirname(os.path.realpath(sys.argv[0]))
shapefile_name = os.path.join(mypath,"../files/tl_2012_us_state.shp")
shapefile = osgeo.ogr.Open(shapefile_name)
numLayers = shapefile.GetLayerCount()

print "Shapefile contains %d layers" % numLayers
print

for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()
    print "Layer %d has spatial reference %s" % (layerNum, spatialRef)
    print "Layer %d has %d features" % (layerNum, numFeatures)
    print

    for featureNum in range(numFeatures):
        feature = layer.GetFeature(featureNum)
        featureName = feature.GetField("NAME")

        print "Feature %d has name %s" % (featureNum, featureName)

