'''
    Fibonacci, the module: this is exactly the same 
    cotent alredy presented in 07 version, but a
    proper name has to be used to be called by
    external scripts.

'''
def fibonacci(n=2000):
    '''
        Compute Fibonacci series and return it as a list
    '''
    a, b = 0, 1
    f = []
    while b<n:
        f.append(a)
        a, b = b, a+b
    return f

if __name__ == "__main__":
    s = fibonacci()
    print s
