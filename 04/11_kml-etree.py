#!/usr/bin/python3

# Parse KML using ElementTree                                                                             try:
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET      
tree = ET.ElementTree(file="../files/time-stamp-point.kml")
ns = "{http://www.opengis.net/kml/2.2}"
placemark = tree.find(".//%sPlacemark" % ns)
coordinates = placemark.find("./%sPoint/%scoordinates" % (ns,ns))
print(coordinates.text)


