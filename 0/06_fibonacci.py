'''
    Keyword arguments in calling functions
'''
def fibonacci(n=2000):
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

s = fibonacci(n=10000)
print s
