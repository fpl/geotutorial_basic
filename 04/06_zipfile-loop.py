#!/usr/bin/python3

# Unzip a shapefile with a for loop
import zipfile
zip = open("../files/hancock.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
  out = open(fileName, "wb")
  out.write(zipShape.read(fileName))
  out.close()
