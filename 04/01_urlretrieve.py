#!/usr/bin/python3

# Retrieve a file using urllib
import urllib.request
url = "http://spatial-ecology.net/dokuwiki/lib/exe/fetch.php?media=wiki:python:hancock.zip"
fileName = "hancock.zip"
urllib.request.urlretrieve(url, fileName)


