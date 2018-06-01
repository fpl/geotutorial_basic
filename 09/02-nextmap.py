import urllib
from xml.dom import minidom
import time

def nextbus(a, r, c="vehicleLocations", e=0):
  """Returns the most recent latitude and 
  longitude of the selected bus line using
  the NextBus API (nbapi)"""
  nbapi = "http://webservices.nextbus.com"
  nbapi += "/service/publicXMLFeed?"
  nbapi += "command=%s&a=%s&r=%s&t=%s" % (c,a,r,e)
  xml = minidom.parse(urllib.urlopen(nbapi))
  bus=xml.getElementsByTagName("vehicle")
  if bus:    
    at = bus[0].attributes
    return(at["lat"].value, at["lon"].value)
  else: return (False, False)

def nextmap(a, r, mapimg, index):
  """Plots a nextbus location on a map image
  and saves it to disk using the OpenStreetMap
  Static Map API (osmapi)"""
  # Fetch the latest bus location
  lat, lon = nextbus(a, r)
  if not lat:
    return False
  # Base url + service path
  osmapi = "http://staticmap.openstreetmap.de/"
  osmapi += "staticmap.php?maptype=mapnik&"
  # Map Image width and height in pixels
  osmapi += "size=800x600" + "&"
  # Center the map on the bus location
  osmapi += "center=%s,%s" % (lat,lon) + "&"
  # Map zoom level (between 1-18)
  osmapi += "zoom=16" + "&"
  # Bus mark location 
  osmapi += "markers=%s,%s,lightblue%d" % (lat, lon, index) 
  print osmapi
  img = urllib.urlopen(osmapi)
  # Save the map image
  with open(mapimg + "%d.png" % index, "wb") as f:
    f.write(img.read())
  return True

# Nextbus API agency and bus line variables
agency = "chapel-hill"
route = "A"

# Name of map image to save as PNG
nextimg = "nextmap"

# Number of updates we want to make
requests = 3

# How often we want to update (seconds)
freq = 5

# Map the bus location every few seconds 
for i in range(requests):
  success = nextmap(agency, route, nextimg, i+1)
  if not success:
    print "No data available."
    continue
  print "Saved map %s at %s" % (i, time.asctime())
  time.sleep(freq)
  
