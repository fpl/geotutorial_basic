import sys
import urllib
from xml.dom import minidom
import math
import Image

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
  
def ll2m(lat,lon):
  """Lat/lon to meters"""
  x = lon * 20037508.34 / 180.0
  y = math.log(math.tan((90.0 + lat) * \
   math.pi / 360.0)) / (math.pi / 180.0)
  y = y * 20037508.34 / 180
  return (x,y)

def wms(minx, miny, maxx, maxy, service, lyr, img, w, h):
  """Retrieve a wms map image from
  the specified service and saves it as a PNG."""
  wms = service
  wms += "?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&"
  wms += "LAYERS=%s" % lyr
  wms += "&STYLES=&"
  wms += "SRS=EPSG:900913&"
  wms += "BBOX=%s,%s,%s,%s&" % (minx,miny,maxx,maxy)
  wms += "WIDTH=%s&" % w
  wms += "HEIGHT=%s&" % h 
  wms += "FORMAT=image/png"
  print wms
  wmsmap = urllib.urlopen(wms)
  with open(img + ".png", "wb") as f:
    f.write(wmsmap.read())

# Nextbus agency and route ids
agency = "thunderbay"
route = "1"

# NOAA OpenStreetMap WMS service
basemap = "http://osm.woc.noaa.gov/mapcache" 

# Name of the WMS street layer
streets = "osm"

# Name of the basemap image to save
mapimg = "basemap"

# OpenWeatherMap.org WMS Service
weather = "http://wms.openweathermap.org/service"

# Type of weather: precipitation|snow|rain|clouds
sky = "precipitation"

# Name of the weather image to save
skyimg = "weather"

# Name of the finished map to save
final = "next-weather"

# Transparency level for weather layer
# when we blend it with the base map.
# 0 = invisible, 1 = no transparency
opacity = .5

# Pixel width and height of the 
# output map images
w = 600
h = 600

# Pixel width/height of the the 
# bus marker icon
icon = 30

# Get the bus location    
lat, lon = nextbus(agency, route)
if not lat:
  print "No bus data available."
  print "Please try again later"
  sys.exit()


# Convert the degrees to meters
# to match the WMS maps
x,y = ll2m(lat, lon) 

# Create a bounding box 1 mile (1600 m)
# in each direction around the bus
minx = x - 1600
maxx = x + 1600
miny = y - 1600
maxy = y + 1600

# Download the street map
wms(minx, miny, maxx, maxy, basemap, streets, mapimg, w, h)   

# Download the weather map
wms(minx, miny, maxx, maxy, weather, sky, skyimg, w, h)

# Open the basemap image in PIL
im1 = Image.open("basemap.png")

# Open the weather image in PIL
im2 = Image.open("weather.png")

# Convert the weather image mode
# to "RGB" from an indexed PNG
# so it matches the basemap image
im2 = im2.convert(im1.mode)

# Create a blended image combining
# the base map with the weather map
im3 = Image.blend(im1,im2,opacity)

# Open up the bus icon image to
# use as a location marker
im4 = Image.open("busicon.png")

# Shrink the icon to the desired
# size
im4.thumbnail((icon,icon))

# Use the blended map image
# and icon sizes to place 
# the icon in the center of
# the image since the map
# is centered on the bus
# location.
w,h = im3.size
w2,h2 = im4.size

# Paste the icon in the center of the image
im3.paste(im4, ((w/2)-(w2/2), (h/2)-(h2/2)), im4)

# Save the finished map
im3.save(final + ".png")