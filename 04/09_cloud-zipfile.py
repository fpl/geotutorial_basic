#!/usr/bin/python3

# Extract a zipped shapefile via a url
import urllib.request
import zipfile
import io
import struct
url = "http://spatial-ecology.net/dokuwiki/lib/exe/fetch.php?media=wiki:python:hancock.zip"
cloudshape = urllib.request.urlopen(url)
memoryshape = io.BytesIO(cloudshape.read())
zipshape = zipfile.ZipFile(memoryshape)
cloudshp = zipshape.read("hancock.shp")
# Access Python string as an array
# read shapefile boundingbox
struct.unpack("<dddd", cloudshp[36:68])
