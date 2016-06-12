# Build kml with eTree
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET      

root = ET.Element("kml")
root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
placemark = ET.SubElement(root, "Placemark")
office = ET.SubElement(placemark, "name")
office.text = "Office"
point = ET.SubElement(placemark, "Point")
coordinates = ET.SubElement(point, "coordinates")
coordinates.text = "-122.087461,37.422069"
tree = ET.ElementTree(root)
tree.write("placemark.kml", xml_declaration=True,encoding='utf-8',method="xml")
