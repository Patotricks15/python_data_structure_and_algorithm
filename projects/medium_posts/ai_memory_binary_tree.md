# Beyond the Queue: How a Binary Search Tree (and a bit of NLP) Makes AI Memory Smarter

In my previous post, we explored how a **Doubly Linked List** can create a super-efficient "Sliding Window" memory for an AI. It’s fast, deterministic, and follows a strict FIFO (First-In, First-Out) rule. But as I kept building, I hit a wall: **Time isn't the same as Importance.**

If you tell an AI your name at the start of a long conversation, a standard sliding window will eventually "forget" it as new, less important messages (like small talk about the weather) push the old ones out. 

To solve this, I decided to level up. We’re moving beyond the simple chain and building a **Hybrid Smart Memory using a Binary Search Tree (BST) and Named Entity Recognition (NER)**.

---

### The Basics: What is a Binary Search Tree?

Before we dive into the AI logic, let’s refresh the basics. A **Binary Tree** is a hierarchical data structure where each node has at most two children, referred to as the **left** and **right** child.

However, we are using a specific type called a **Binary Search Tree (BST)**. A BST follows a very strict rule for every single node:
1.  All values in the **left subtree** are **less than** the node’s value.
2.  All values in the **right subtree** are **greater than** the node’s value.

#### Why is this efficient?
In a regular list, if you want to find a specific item, you have to look at everything one by one (**O(n)**). In a balanced BST, every move you make down the tree cuts the remaining search area in half. This gives us a search complexity of **O(log n)**. 

---

### The Architecture: Our Memory Node

Instead of a simple list entry, we structure our "Memory Boxes" as nodes. In Python, we use `@dataclass` to keep the code clean and modern:

```python
@dataclass
class MemoryNode:
    importance: float  # Our BST Key (0.0 to 10.0)
    content: str
    role: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Binary Tree pointers (Pointers to children)
    left: Optional['MemoryNode'] = field(default=None, repr=False)
    right: Optional['MemoryNode'] = field(default=None, repr=False)
```

---

### Phase 1: The Hybrid Scoring System (LLM + NER)

Re-evaluating importance is the core of this project. To make the system robust, I implemented a **Hybrid Scorer** that combines the subjective intuition of an LLM with the deterministic power of **SpaCy**.

Here is how we instruct the LLM using **LangChain** to act as our judge:

```python
self.scorer_prompt = ChatPromptTemplate.from_template(
    "Evaluate the IMPORTANCE of the USER's last message (0.0 to 10.0) "
    "to be remembered in FUTURE conversations.\n\n"
    "RULES:\n"
    "- 9.5-10.0: CRITICAL DATA (Names, addresses, vital facts).\n"
    "- 7.5-9.0: PERSISTENT PREFERENCES (Specific tastes, hobbies).\n"
    "- 0.0-1.4: SMALL TALK (Greetings, 'how are you').\n\n"
    "Respond ONLY with the decimal number."
)
```

And then we merge it with our local NER scanner:

```python
def _get_importance_score(self, text: str) -> float:
    # 1. Subjective Judge: LLM evaluates context
    llm_score = self.llm_chain.invoke({"message": text})
    
    # 2. Objective Scanner: NER counts factual entities (Names, Dates, Locations)
    doc = self.nlp(text)
    ner_score = len(doc.ents) * 2.5 # 2.5 points per entity
    
    # 3. Hybrid Max: We take the best of both worlds
    return min(max(llm_score, ner_score), 10.0)
```

---

### Phase 2: Efficient Retrieval via "Reverse In-order Traversal"

A tree is only as good as how you climb it. We use **Reverse In-order Traversal** (Right -> Root -> Left) to visit the nodes in descending order of value.

```python
def _reverse_inorder(self, node: Optional[MemoryNode], memories: List[Dict], limit: int):
    if node is None or len(memories) >= limit:
        return
        
    self._reverse_inorder(node.right, memories, limit) # Visit Higher values first
    if len(memories) < limit:
        memories.append(node)
    self._reverse_inorder(node.left, memories, limit)
```

---

### Phase 3: The "Memory Wrapped" (Final Summarization)

At the end of the session, we use a recursive function to collect every node with a score of **7.0 or higher**. This "Elite" context is then summarized by the LLM to create a persistent User Profile.

```python
def generate_final_summary(self):
    # Collect nodes >= 7.0 from the tree
    high_val_memories = self.memory.get_high_importance_memories(threshold=7.0)
    
    context_str = "\n".join(high_val_memories)
    
    summary_prompt = ChatPromptTemplate.from_template(
        "Based on these high-importance memories, generate a concise summary "
        "of what we learned about the user and their main goals:\n\n"
        "{memories}\n\nSUMMARY:"
    )
    
    return self.chat_llm.invoke({"memories": context_str})
```

---

### Visualizing the Structure

The beauty of a BST is its visual hierarchy. By implementing an ASCII printer, we can see exactly how the AI is "weighting" our conversation:

```text
--- Memory Structure Visualization (BST) ---
└── [1.5] USER: Hello there!
    ├── [9.8] USER: My name is Patrick and I love Python.
    │   └── [10.0] USER: My meeting is at 3PM in London.
    └── [3.0] ASSISTANT: Hello Patrick! How can I help?
```

---

### Why this matters for the future of AI

As we move toward **Long-term AI Agents**, we can't keep feeding them 100% of our chat history. It's too expensive and creates "noise" that confuses the model. Structures like **Binary Search Trees** are the future. They move us away from "storing strings" and toward "organizing knowledge."

---
*If you're interested in the code for this project, check out my repo [Link to Repo]. Stay tuned for the next part, where we explore how to turn this tree into a fully-searchable Vector Database!*
