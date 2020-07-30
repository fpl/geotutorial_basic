#!/usr/bin/python3

# Examine and update a dbf file with dbfpy
from dbfpy import dbf
db = dbf.Dbf("../files/GIS_CensusTract_poly.dbf")
print db[0]
rec = db[0]
field = rec["POPULAT10"]
rec["POPULAT10"] = field
rec["POPULAT10"] = field+1
rec.store()
del rec
print(db[0]["POPULAT10"])

