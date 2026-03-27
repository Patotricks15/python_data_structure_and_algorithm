import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class MessageNode:
    """
    Represents an AI chat message with metadata.
    """
    role: str          # "user" or "assistant"
    content: str
    token_count: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Linked list pointers (excluded from repr to avoid recursion)
    next: Optional['MessageNode'] = field(default=None, repr=False)
    prev: Optional['MessageNode'] = field(default=None, repr=False)

class ChatMemory:
    """
    Advanced Doubly Linked List memory for AI context.
    """
    def __init__(self, limit: int = 5):
        self.head: Optional[MessageNode] = None
        self.tail: Optional[MessageNode] = None
        self.size: int = 0
        self.limit: int = limit

    def _calculate_tokens(self, text: str) -> int:
        """Simple token count simulation (word count)."""
        return len(text.split())

    def add_message(self, role: str, content: str):
        """Adds a message with auto-generated metadata."""
        tokens = self._calculate_tokens(content)
        new_node = MessageNode(role=role, content=content, token_count=tokens)

        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size += 1

        if self.size > self.limit:
            self.remove_oldest()

    def remove_oldest(self):
        """Removes the oldest message (FIFO). O(1)."""
        if not self.head:
            return

        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1

    def get_messages(self) -> List[Dict]:
        """Returns all messages with their metadata."""
        history = []
        current = self.head
        while current:
            history.append({
                "id": current.id,
                "timestamp": current.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "role": current.role,
                "content": current.content,
                "tokens": current.token_count
            })
            current = current.next
        return history

    def clear(self):
        """Wipes memory."""
        self.head = self.tail = None
        self.size = 0

# --- Test ---
if __name__ == "__main__":
    memory = ChatMemory(limit=2)
    
    memory.add_message("user", "Hello computer!")
    memory.add_message("assistant", "Hello human! How can I help you today?")
    memory.add_message("user", "What is your purpose?")

    print(f"Memory size (Limit 2): {memory.size}\n")
    for msg in memory.get_messages():
        print(f"[{msg['timestamp']}] ID: {msg['id'][:8]}...")
        print(f"{msg['role'].upper()} ({msg['tokens']} tokens): {msg['content']}\n")
