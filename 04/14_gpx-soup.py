#!/usr/bin/python3

# Parse broken GPX data with BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
gpx = open("../files/broken_data.gpx")
soup = BeautifulStoneSoup(gpx.read())
# Check the first track point
print(soup.trkpt)
# Find the rest of the track points and count them
tracks = soup.findAll("trkpt")
print(len(tracks))                                                                            
# Save the fixed xml file
fixed = open("fixed_data.gpx", "w")
fixed.write(soup.prettify())
fixed.close()

