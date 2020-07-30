'''
Now use a class instead of a procedural module
'''
import sys
from FibonacciBasic import Fibonacci as f

def usage():
    print '''\
usage: %s int \
''' % sys.argv[0]
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

try:
    n = int(sys.argv[1])
except:
    usage()

s = f(n)
s.list()
