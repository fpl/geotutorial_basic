#!/usr/bin/python3

# Extract a shapefile from a gzipped tar archive
import tarfile
tar = tarfile.open("hancock.tar.gz", "r:gz")
tar.extractall()
tar.close()
