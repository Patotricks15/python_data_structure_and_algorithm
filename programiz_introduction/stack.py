class Stack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        """
        Add an element to the top of the stack.

        :param element: Element to add to the stack
        :type element: Any
        """
        self.stack.append(element)
    
    def pop(self):
        """
        Remove and return the top element of the stack.
        
        :return: The top element of the stack or "Stack is empty"
        :rtype: Any
        """
        if self.isEmpty():
            return "Stack is empty"
        return self.stack[:-1]
    def peek(self):
        """
        Return the top element of the stack without removing it.

        :return: The top element of the stack or "Stack is empty"
        :rtype: Any
        """
        if self.isEmpty():
            return "Stack is empty"
        return self.stack[-1]

    def isEmpty(self):
        """
        Check if the stack is empty.

        :return: If the stack is empty
        :rtype: bool
        """
        return len(self.stack) == 0
    
    def size(self):
        """
        Return the size of the stack.
        
        :return: The size of the stack
        :rtype: int
        """
        return len(self.stack)
    
# Create a stack
myStack = Stack()

myStack.push('A')
myStack.push('B')
myStack.push('C')
print("Stack: ", myStack.stack)

print("Pop: ", myStack.pop())

print("Peek: ", myStack.peek())

print("isEmpty: ", myStack.isEmpty())

print("Size: ", myStack.size())