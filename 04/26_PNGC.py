#!/usr/bin/python3

# Rasterize a shapefile with PNGCanvas
import shapefile
import pngcanvas
r = shapefile.Reader("../files/hancock.shp")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 400
iheight = 600
xratio = iwidth/xdist
yratio = iheight/ydist
pixels = []
for x,y in r.shapes()[0].points:
  px = int(iwidth - ((r.bbox[2] - x) * xratio))
  py = int((r.bbox[3] - y) * yratio)
  pixels.append([px,py])
c = pngcanvas.PNGCanvas(iwidth,iheight)
c.polyline(pixels)
f = file("hancock_pngcvs.png", "wb")
f.write(c.dump())
f.close()
