'''
    FibonacciAdvanced, the OOP approach
'''
class FibonacciAdvanced:
    ''' 
    This is a class with a static member and 
    a static method
    '''

    # static member
    _name = 'Fibonacci series advanced class' 

    def __init__(self, n=2000):
        self._f = []
        a, b = 0, 1
        while b<n:
            self._f.append(a)
            a, b = b, a+b

    def list(self):
        print self._f

    def get(self,index=0):
        print self._f[index]

    def slice(self,start=0,end=-1):
        print self._f[start:end]

    # static method with mandatory decorator
    @staticmethod 
    def name():
        return FibonacciAdvanced._name

'''
    This is a base class with inherited classes
'''

class Sequence(object):

    def __init__(self, a, b, n=2000):
        self._f = []
        while b<n:
            self._f.append(a)
            a, b = b, a+b

    def list(self):
        print self._f

    def get(self,index=0):
        print self._f[index]

    def slice(self,start=0,end=-1):
        print self._f[start:end]

class Fibonacci(Sequence):

    def __init__(self, n=2000):
        Sequence.__init__(self,0,1,n)

class Lucas(Sequence):

    def __init__(self, n=2000):
        Sequence.__init__(self,2,1,n)

class FibonacciSuper(Sequence):
    def __init__(self, n=2000):
        super(FibonacciSuper,self).__init__(2,1,n)
        '''
        super(self.__class__,self).__init__(2,1,n)      # An alternative way in 2.7
        Sequence.__init__(self,2,1,n)                   # Another alternative
        super().__init__(2,1,n)     # The 3.0 way...
        '''

#
# ... and all together
#

if __name__ == "__main__":
    u = FibonacciAdvanced(10000)
    s = Fibonacci(10000)
    t = Lucas(100000)
    v = FibonacciSuper(1000000000000000000)

    u.list()
    print 'This is a static method call: ' + FibonacciAdvanced.name()

    s.list()
    s.get()
    s.get(11)
    s.slice(11,15)

    t.list()
    t.get()
    t.get(11)
    t.slice(11,15)

    v.list()
