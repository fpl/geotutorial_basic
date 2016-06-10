# Read FTP data via the web
import urllib
ftpURL = "ftp://anonymous:anonymous@"
dart = urllib.urlopen(ftpURL + server + "/" + dir + "/" + fileName)
for line in dart:
  if "LAT," in line:
    print line
    break
