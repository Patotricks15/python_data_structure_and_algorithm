from collections import deque

queue = deque()

queue.append(1)
queue.append(2)
queue.append(3)
print(queue)  

first = queue.popleft()
print(first)
print(queue)

first = queue[0]
print(first)
