arr = [3, 7, 2, 9, 5]
targetVal = 9
def linear_search(arr, targetVal):
    for i in range(len(arr)):
        if arr[i] == targetVal:
            return i
        

print(linear_search(arr, targetVal))