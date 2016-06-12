# Retrieve a file using urllib
import urllib
url = "http://spatial-ecology.net/dokuwiki/lib/exe/fetch.php?media=wiki:python:hancock.zip"
fileName = "hancock.zip"
urllib.urlretrieve(url, fileName)


