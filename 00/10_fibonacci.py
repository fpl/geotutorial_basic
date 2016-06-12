'''
    Command line parameters
'''
import sys
from fibonacci import fibonacci

s = fibonacci(int(sys.argv[1]))
print s
