'''
    Preparing for modules...
'''
def fibonacci(n=2000):
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

if __name__ == "__main__":
    s = fibonacci()
    print len(s)

print s

