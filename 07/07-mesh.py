"""
Convert an LAS LIDAR file to a shapefile
by creating a 3D triangle mesh using
Delaunay Triangulation.
"""
# cPickle is used to store
# tessalated triangles
# to save time writing 
# future shapefiles
import cPickle
import os
import time
import math
# Third-party Python modules:
import numpy as np
import shapefile
from laspy.file import File
import voronoi

# Source LAS file
source = "clippedLAS.las"

# Output shapefile
target = "mesh"

# Triangles archive
archive = "triangles.p"

# Pyshp archive
pyshp = "mesh_pyshp.p"

# Point class required by
# the voronoi module
class Point:
  def __init__(self,x,y):
    self.px = x
    self.py = y
  
  def x(self):
    return self.px
  
  def y(self):
    return self.py

# This will be the triangle
# array.  Load it from a pickle
# file or use the voronoi module
# to create the triangles.
triangles = None

if os.path.exists(archive):
  print "Loading triangle archive..."
  f = open(archive, "rb")
  triangles = cPickle.load(f)
  f.close()
  # Open LIDAR LAS file
  las = File(source, mode="r")  
else:
  # Open LIDAR LAS file
  las = File(source, mode="r")  
  points = []
  print "Assembling points..."  
  # Pull points from LAS file
  for x,y in np.nditer((las.x,las.y)): 
    points.append(Point(x,y))
  print "Composing triangles..."
  # Delaunay Triangulation  
  triangles = voronoi.computeDelaunayTriangulation(points) 
  # Save the triangles to save time if we write more than
  # one shapefile.
  f = open(archive, "wb")
  cPickle.dump(triangles, f, protocol=2)
  f.close()
  
print "Creating shapefile..."
w = None 
if os.path.exists(pyshp):
  f = open(pyshp, "rb")
  w = cPickle.load(f)
  f.close()
else:
  # PolygonZ shapefile (x,y,z,m)
  w = shapefile.Writer(shapefile.POLYGONZ)
  w.field("X1", "C", "40")
  w.field("X2", "C", "40")
  w.field("X3", "C", "40")
  w.field("Y1", "C", "40")
  w.field("Y2", "C", "40")
  w.field("Y3", "C", "40")
  w.field("Z1", "C", "40")
  w.field("Z2", "C", "40")
  w.field("Z3", "C", "40")
  tris = len(triangles)
  # Loop through shapes and 
  # track progress every 10 percent
  last_percent = 0
  for i in range(tris):
    t = triangles[i]
    percent = int((i/(tris*1.0))*100.0)
    if percent % 10.0 == 0 and percent > last_percent:
      last_percent = percent
      print "%s %% done - Shape %s/%s at %s" % (percent, i, tris, time.asctime()) 
    part=[]
    x1 = las.x[t[0]]
    y1 = las.y[t[0]]
    z1 = las.z[t[0]]
    x2 = las.x[t[1]]
    y2 = las.y[t[1]]
    z2 = las.z[t[1]]
    x3 = las.x[t[2]]
    y3 = las.y[t[2]]
    z3 = las.z[t[2]]
    # Check segments for large triangles
    # along the convex hull which is an common
    # artificat in Delaunay triangulation
    max = 3
    if math.sqrt((x2-x1)**2+(y2-y1)**2) > max: continue
    if math.sqrt((x3-x2)**2+(y3-y2)**2) > max: continue
    if math.sqrt((x3-x1)**2+(y3-y1)**2) > max: continue
    part.append([x1,y1,z1,0])
    part.append([x2,y2,z2,0])
    part.append([x3,y3,z3,0])
    w.poly(parts=[part])
    w.record(x1,x2,x3,y1,y2,y3,z1,z2,z3)
  print "Saving shapefile..."
  # Pickle the Writer in case something
  # goes wrong. Be sure to delete this
  # file to recreate teh shapefile.
  f = open(pyshp, "wb")
  cPickle.dump(w, f, protocol=2)
  f.close()
w.save(target)
print "Done."
  

