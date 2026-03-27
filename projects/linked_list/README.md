# AI Chat Memory: Doubly Linked List Implementation

This project implements a Dynamic Chat Memory system for an AI Assistant using a Doubly Linked List in Python. It simulates how modern AI models manage their limited context window using a "Sliding Window" strategy.

## Why This Approach?

While a standard Python list could be used, it is inefficient for memory management at scale:
*   Python List Pop(0): Removing the first element from a standard list is O(n) because every other element must be shifted.
*   Linked List Removal: Removing the "Head" (oldest message) in a Linked List is O(1), making it much more efficient for real-time memory management.

## Key Features

*   O(1) Operations: Both adding a new message (Tail) and removing the oldest (Head) happen in constant time.
*   Metadata Rich Nodes: Every message is a MessageNode containing:
    *   ID: Unique UUID for tracking.
    *   Timestamp: Precise creation time.
    *   Token Count: Simulated context tracking.
    *   Role & Content: The actual message data.
*   Modern Python: Uses @dataclass for cleaner code and automatic handling of metadata defaults.
*   Sliding Window: Automatically purges the oldest messages when the defined limit is reached to keep token usage within bounds.

## Performance Analysis

| Operation | Time Complexity | Note |
| :--- | :--- | :--- |
| Add Message | O(1) | Append directly to the tail. |
| Remove Oldest | O(1) | Shift the head pointer. |
| Get Full History | O(n) | Linear traversal of the list. |
| Find Keyword | O(n) | Standard linear search. |

## Usage Example

```python
from AI_memory import ChatMemory

# Initialize memory with a 3-message limit
memory = ChatMemory(limit=3)

# Adding messages
memory.add_message("user", "Hello computer!")
memory.add_message("assistant", "Hello! How can I help?")
memory.add_message("user", "Explain Linked Lists.")
memory.add_message("assistant", "Sure! They are nodes connected by pointers...")

# The oldest message ("Hello computer!") is already purged!
print(memory.get_messages())
```

## Portfolio Summary

"Designed and implemented an AI-oriented memory management system using a Doubly Linked List in Python. Integrated UUID generation, timestamp tracking, and O(1) sliding window purgation to optimize context handling, demonstrating knowledge of both low-level data structure optimization and modern AI system design."
