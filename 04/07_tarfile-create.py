#!/usr/bin/python3

# Add a shapefile to a tar archive
import tarfile
tar = tarfile.open("hancock.tar.gz", "w:gz")
tar.add("hancock.shp")
tar.add("hancock.shx")
tar.add("hancock.dbf")
tar.close()
