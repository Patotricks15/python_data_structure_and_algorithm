my_array = [7, 12, 9, 4, 11]
maxVal = my_array[0]

for i in my_array:
    if i > maxVal:
        maxVal = i

print('Highest value:',maxVal)