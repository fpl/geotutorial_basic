'''
  Use of a function
'''
def fibonacci(n):
    a, b = 0, 1
    while b<n:
        print a
        a, b = b, a+b

fibonacci(2000)
