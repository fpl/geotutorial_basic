"""
fmtDecode.py - Simple program to manually decode binary formats.
"""

import struct
import pickle
import os

def export():
    print "Saving results"
    out = None
    if cached:
      out = file(oname, "a")
    else:
      out = file(oname, "w")
      out.write(header)
    for record in fileDesc:
        for field in record:
            out.write("%s\t" % field)
        out.write("\n")
    out.close()
    pickle.dump(cached, file(pickleJar, "w"))

header = "POSTION\tFIELD\tSAMPLE\tTYPE\tBYTE_ORDER\n"
fileDesc = []
files = os.listdir(".")
count = 1
print "Available Files:"

for f in files:
  print " %s. %s" % (count, f)
  count += 1

fnum = raw_input("Enter the number of the file to decode: ")
fname = files[int(fnum)-1]
base = os.path.splitext(fname)[0]

pickleJar = "%s.p" % base

cached = []

if os.path.exists(pickleJar):
    print "Cached session available."
    print 
    useCache = raw_input("Use it? Yes (Y), No (N)?")
    if "y" in useCache.lower() or useCache == "":
        cached = pickle.load(open(pickleJar, "r"))
    else: cached = []

oname = "%s_decode.txt" % base

f = open(fname, "rb")
loc = f.tell()
f.seek(0,2)
eof = f.tell()
f.seek(0)
prev = 0

if len(cached)>0:
    print "Using cache..."
    f.seek(cached[-1])
    prev = cached[-2]
    
print "Starting at byte %s..." % f.tell()

try:
    formats = {"char":{"format":"c","len":1},
               "signed char":{"format":"b","len":1},
               "unsigned char":{"format":"B","len":1},
               "_Bool":{"format":"?","len":1},
               "short":{"format":"h","len":2},
               "unsigned short":{"format":"h","len":2},
               "int":{"format":"i","len":4},
               "unsigned int":{"format":"I","len":4},
               "long":{"format":"l","len":4},
               "unsigned long":{"format":"L","len":4},
               "long long":{"format":"q","len":8},
               "unsigned long long":{"format":"Q","len":8},
               "float":{"format":"f","len":4},
               "double":{"format":"d","len":8}}
               
    while f.tell() < eof:
        record = []
        start = f.tell()
        record.append("%s\t" % start)
        cached.append(start)
        fields = []
        print 
        count = 1
        try:
          # Little endian formats
          for fmt in formats:
            form = formats[fmt]["format"]
            bytes = formats[fmt]["len"]
            field = struct.unpack("<%s" % form, f.read(bytes))
            print "%s. Little %s: %s" % (count, fmt, field)
            count += 1
            f.seek(start)
            fields.append([str(field[0]), fmt, "little", str(bytes)])
        except: pass                  

        try:
          # Big endian formats
          for fmt in formats:
            form = formats[fmt]["format"]
            bytes = formats[fmt]["len"]
            field = struct.unpack(">%s" % form, f.read(bytes))
            print "%s. Big %s: %s" % (count, fmt, field)
            count += 1
            f.seek(start)
            fields.append([str(field[0]), fmt, "big", str(bytes)])
        except: pass                  

        print "%s. Go back to previous" % count
        print
        print "Current location: %s" % f.tell()
        choice = raw_input("Enter the number of one of the above options: ")
        choice = int(choice.strip())
        desc = ""
        if choice != count:
          desc = raw_input("Enter a field description: ")
          record.append("%s\t" % desc)
          record.append("%s\t" % fields[choice-1][0])
          record.append("%s\t" % fields[choice-1][1])
          record.append("%s\t" % fields[choice-1][2])
          f.seek(start + int(fields[choice-1][3]))
          prev = start
          fileDesc.append(record)
        elif choice == count:
            f.seek(prev)
            print "Going back to previous field."          
    f.close()
    export()
except KeyboardInterrupt:
    print
    reverse = input("How many records back? ")
    for i in range(reverse):
        cached.pop()
    pickle.dump(cached, file(pickleJar, "w"))
    print "The program will exit.  Restart and use cached version."
    
except:
    export()
     
    
        
        
        
    
