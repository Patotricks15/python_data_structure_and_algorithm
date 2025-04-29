class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        
        self.head = None
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            print("new node:", new_node.data)
        else:
            last = self.head
            while last.next:
                last = last.next
            last.next = new_node
            print("Appended:", data)
    def print_list(self):
        """
        Prints out the linked list in the format 1 -> 2 -> 3 -> None
        """
        current = self.head
        while current:
            print(current.data, end = " -> ")
            current = current.next
        print("None")

ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.print_list() 