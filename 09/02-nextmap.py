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
    at = bus.attributes
    return(at["lat"].value, at["lon"].value)
  else: return (False, False)

def nextmap(a, r, mapimg):
  """Plots a nextbus location on a map image
  and saves it to disk using the OpenStreetMap
  Static Map API (osmapi)"""
  # Fetch the latest bus location
  lat, lon = nextbus(a, r)
  if not lat:
    return False
  # Base url + service path
  osmapi = "http://ojw.dev.openstreetmap.org/"
  osmapi += "StaticMap/?mode=API&"
  # Show=1 returns an image
  osmapi += "show=1" + "&"
  # fmt can be "png" or "jpg" map image format
  osmapi += "fmt=png" + "&"
  # Remove the map image attribute label
  osmapi += "att=none" + "&"
  # Map Image width and height in pixels
  osmapi += "w=800" + "&"
  osmapi += "h=600" + "&"
  # Center the map on the bus location
  osmapi += "lat=%s&" % lat
  osmapi += "lon=%s&" % lon 
  # Map zoom level (between 1-18)
  osmapi += "zoom=16" + "&"
  # Bus mark location 
  osmapi += "mlat0=%s&" % lat 
  osmapi += "mlon0=%s&" % lon
  # Bus marker OpenStreetMap icon id
  # (blue dot id=30326) 
  osmapi += "mico0=30326"
  img = urllib.urlopen(osmapi)
  # Save the map image
  with open(mapimg + ".png", "wb") as f:
    f.write(img.read())
  return True

# Nextbus API agency and bus line variables
agency = "thunderbay"
route = "1"

# Name of map image to save as PNG
nextimg = "nextmap"

# Number of updates we want to make
requests = 3

# How often we want to update (seconds)
freq = 5

# Map the bus location every few seconds 
for i in range(requests):
  success = nextmap(agency, route, nextimg)
  if not success:
    print "No data available."
    continue
  print "Saved map %s at %s" % (i, time.asctime())
  time.sleep(freq)
  