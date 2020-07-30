#!/usr/bin/python3
"""
structDemo.py - demonstrate using the struct module
by reading the bounding box from a shapefile. 
"""
import struct
# Open the shapefile
f = open("../files/hancock.shp","rb")
# Go to the start of the
# bounding box coordinates
f.seek(36)
# Read min-x,min-y,max-x,max-y
# in little endian format
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
# Read all 4 values at once
f.seek(36)
print(struct.unpack("<dddd", f.read(32)))
