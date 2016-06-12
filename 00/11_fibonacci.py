'''
    What if you call this script without the required
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

s = fibonacci(int(sys.argv[1]))
print s
