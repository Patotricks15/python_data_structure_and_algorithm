import sys

def mergeSort(arr, depth=0):
    indent = '  ' * depth
    print(f"{indent}mergeSort called on {arr}")
    if len(arr) <= 1:
        print(f"{indent}return (base case) {arr}")
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    print(f"{indent}Split into {left} and {right}")

    sortedLeft = mergeSort(left, depth + 1)
    sortedRight = mergeSort(right, depth + 1)

    merged = merge(sortedLeft, sortedRight, depth + 1)
    print(f"{indent}Merged {sortedLeft} and {sortedRight} into {merged}")
    return merged

def merge(left, right, depth):
    indent = '  ' * depth
    print(f"{indent}merge called on {left} and {right}")
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    if i < len(left):
        print(f"{indent}Appending remaining from left: {left[i:]}")
    if j < len(right):
        print(f"{indent}Appending remaining from right: {right[j:]}")
    result.extend(left[i:])
    result.extend(right[j:])
    print(f"{indent}Result of merge: {result}")
    return result

unsortedArr = [3, 7, 6, -10, 15, 23.5, 55, -13]
print("Unsorted array:", unsortedArr)
sortedArr = mergeSort(unsortedArr)
print("Sorted array:", sortedArr)
