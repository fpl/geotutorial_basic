def fibonacci(n):
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

s = fibonacci(2000)
print s
