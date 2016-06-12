# Extract a zipped shapefile via a url
import urllib
import zipfile
import StringIO
import struct
url = "http://spatial-ecology.net/dokuwiki/lib/exe/fetch.php?media=wiki:python:hancock.zip"
cloudshape = urllib.urlopen(url)
memoryshape = StringIO.StringIO(cloudshape.read())
zipshape = zipfile.ZipFile(memoryshape)
cloudshp = zipshape.read("hancock.shp")
# Access Python string as an array
# read shapefile boundingbox
struct.unpack("<dddd", cloudshp[36:68])
