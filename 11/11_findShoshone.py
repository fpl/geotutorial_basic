# findShoshone.py

import pyproj

distance = 132.7 * 1000
angle    = 270.0

f = file("data/NationalFile_20121001.txt", "r")
for line in f.readlines():
    chunks = line.rstrip().split("|")
    if chunks[1] == "Shoshone" and \
       chunks[2] == "Populated Place" and \
       chunks[3] == "CA":
        latitude = float(chunks[9])
        longitude = float(chunks[10])

        geod = pyproj.Geod(ellps='WGS84')
        newLong,newLat,invAngle = geod.fwd(longitude,
                                           latitude,
                                           angle, distance)

        print "Shoshone is at %0.4f,%0.4f" % (latitude,
                                              longitude)
        print "The point %0.2f km west of Shoshone " \
            % (distance/1000.0) \
            + "is at %0.4f, %0.4f" % (newLat, newLong)

f.close()

