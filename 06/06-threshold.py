"""Threshold an image to black and white"""
import gdalnumeric

# Input file name (thermal image)  
src = "islands.tif"

# Output file name
tgt = "islands_classified.tiff"

# Load the image into numpy using gdal
srcArr = gdalnumeric.LoadFile(src)

# Split the histogram into 20 bins as our classes
classes = gdalnumeric.numpy.histogram(srcArr, bins=2)[1]

lut = [[255,0,0],[0,0,0],[255,255,255]]

# Starting value for classification
start = 1

# Set up the output image
rgb = gdalnumeric.numpy.zeros((3, srcArr.shape[0], srcArr.shape[1],), gdalnumeric.numpy.float32)
       
# Process all classes and assign colors
for i in range(len(classes)):
    mask = gdalnumeric.numpy.logical_and(start <= srcArr, srcArr <= classes[i])
    for j in range(len(lut[i])):
        rgb[j] = gdalnumeric.numpy.choose(mask, (rgb[j], lut[i][j]))
    start = classes[i]+1 

# Save the image    
gdalnumeric.SaveArray(rgb.astype(gdalnumeric.numpy.uint8), tgt, format="GTIFF", prototype=src)

