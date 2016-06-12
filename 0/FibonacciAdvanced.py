'''
    FibonacciAdvanced, the OOP approach
'''
class FibonacciAdvanced:

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

    @staticmethod 
    def name():
        return FibonacciAdvanced._name

if __name__ == "__main__":
    s = FibonacciAdvanced(10000)
    s.list()
    s.get()
    s.get(11)
    s.slice(11,15)
    print s.name()
