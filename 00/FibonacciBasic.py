'''
    FibonacciBasic, the OOP approach
'''
class Fibonacci:
    _f = []

    def __init__(self, n=2000):
        a, b = 0, 1
        while b<n:
            self._f.append(a)
            a, b = b, a+b

    def list(self):
        print self._f

if __name__ == "__main__":
    s = Fibonacci(10000)
    s.list()
