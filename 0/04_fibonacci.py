'''
    A true function with a return value and
    a list variable
'''
def fibonacci(n):
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

s = fibonacci(2000)
print s
