print(0)
print(1)

count = 2

def fibonacci(a, b):
    global count
    if count <= 19:
        c = a + b
        print(c)

        count += 1
        a = b
        b = c
        fibonacci(a, b)
    else:
        return False
fibonacci(0, 1)