'''
    Default arguments in functions
'''
def fibonacci(n=2000):
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

s = fibonacci()
print s
