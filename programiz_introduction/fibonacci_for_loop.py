# Two variables to hold the previous two Fibonacci numbers
a = 0
b = 1

print(a)
print(b)

for i in range(18): # A for loop that runs 18 times
    c = a+b #Create new Fibonacci numbers by adding the two previous ones
    print(c) # Print the new Fibonacci number
    a = b  # Update the variables that hold the previous two fibonacci numbers
    b = c  # Update the variables that hold the previous two fibonacci numbers