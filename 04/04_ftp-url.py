#!/usr/bin/python3 

# Read FTP data via the web
import urllib.request
ftpURL = "ftp://anonymous:anonymous@"
server = "ftp.ngdc.noaa.gov"
dir = "hazards/DART/20070815_peru"
fileName = "21415_from_20070727_08_55_15_tides.txt"
dart = urllib.request.urlopen(ftpURL + server + "/" + dir + "/" + fileName)
for line in dart:
  if b"LAT," in line:
    print(line)
    break
