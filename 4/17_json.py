# Parse GeoJson data
jsdata = """{ "type": "Feature", "id": "OpenLayers.Feature.Vector_314", "pro
perties": {}, "geometry": { "type": "Point", "coordinates": [ 97.03125, 39.72656
25 ] }, "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.
3:CRS84" } } }"""
# Try to eval() the data
point = eval(jsdata)
print point["geometry"]
# Use the json module
import json
print json.loads(jsdata)
# Parse and then dump GeoJSON
pydata = json.loads(jsdata)
print json.dumps(pydata)


