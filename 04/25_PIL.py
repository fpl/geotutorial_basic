#!/usr/bin/python3

# Rasterize a shapefile with PIL
import shapefile
from PIL import Image, ImageDraw
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
  pixels.append((px,py))
img = Image.new("RGB", (iwidth, iheight), "white")
draw = ImageDraw.Draw(img)
draw.polygon(pixels, outline="rgb(203, 196, 190)", fill="rgb(198, 204, 189)")
img.save("hancock.png")
