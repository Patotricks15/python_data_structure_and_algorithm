import array

arr = array.array('i', [1, 2, 3, 4, 5])

print(arr[2])

arr[2] = 10
print(arr)
arr.append(6)
print(arr)