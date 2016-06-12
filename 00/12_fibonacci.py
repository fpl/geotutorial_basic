'''
    What if you call this script with a wrong type
    parameter?
'''
import sys
from fibonacci import fibonacci

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

s = fibonacci(n)
print s
