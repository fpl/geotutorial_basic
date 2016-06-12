"""Perform a simple difference image change detection on a 
'before' and 'after' image."""
import gdal, gdalnumeric
import numpy as np

# "Before" image
im1 = "before.tif"
# "After" image
im2 = "after.tif"
# Load before and after into arrays
ar1 = gdalnumeric.LoadFile(im1).astype(np.int8)                                 
ar2 = gdalnumeric.LoadFile(im2)[1].astype(np.int8)
# Perform a simple array difference on the images
diff = ar2 - ar1
# Set up our classification scheme to try
# and isolate significant changes
classes = np.histogram(diff, bins=5)[1]
# The color black is repeated to mask insignificant changes
lut = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,255,0],[255,0,0]]
# Starting value for classification
start = 1
# Set up the output image
rgb = np.zeros((3, diff.shape[0], diff.shape[1],), np.int8)       
# Process all classes and assign colors
for i in range(len(classes)):
    mask = np.logical_and(start <= diff, diff <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = np.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1
# Save the output image
gdalnumeric.SaveArray(rgb, "change.tif", format="GTiff", prototype=im2)
