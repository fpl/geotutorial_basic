#!/usr/bin/python3

# Build KML manually using strings
xml = """<?xml version="1.0" encoding="utf-8"?>"""
xml += """<kml xmlns="http://www.opengis.net/kml/2.2">"""
xml += """  <Placemark>"""
xml += """    <name>Office</name>"""
xml += """    <description>Office Building</description>"""
xml += """    <Point>"""
xml += """      <coordinates>"""
xml += """        -122.087461,37.422069"""
xml += """      </coordinates>"""
xml += """    </Point>"""
xml += """  </Placemark>"""
xml += """</kml>"""
print(xml)
