# Queues - Practical Projects

This folder contains practical projects built using the Queue data structure in Python.

---

## What is a Queue?

A Queue follows the FIFO rule:

> First In, First Out

Think of a real-life line at a coffee shop:
- The first person to arrive is the first person to be served.
- New people always join at the back of the line.
- The attendant always serves from the front of the line.

### Key Operations

| Operation  | What it does                              | Method used    |
|------------|-------------------------------------------|----------------|
| enqueue    | Adds an item to the back of the queue    | append(item)   |
| dequeue    | Removes item from the front               | popleft()      |
| peek       | Looks at the front item (no removal)      | queue[0]       |
| is_empty   | Checks if the queue has no items          | len() == 0     |

---

## Projects

### 1. Customer Service Simulator (customer_service_sim.py)

Simulates a support desk where customers arrive and wait in line to be served.

**Concepts covered:**
- Basic Queue class (FIFO logic)
- @dataclass for the Customer model
- enqueue / dequeue / peek / display
- Interactive terminal menu

**How to run:**
```bash
python3 projects/queues/customer_service_sim.py
```

---

### 2. Task Scheduler (task_scheduler.py)

Simulates how an operating system or web server handles background tasks.
Implements two types of queues side by side so you can compare them.

**Concepts covered:**
- SimpleQueue - basic FIFO (tasks run in arrival order)
- PriorityQueue - uses Python's heapq (most urgent tasks run first)
- @dataclass for the Task model
- Priority levels: HIGH (1), MEDIUM (2), LOW (3)

**How to run:**
```bash
python3 projects/queues/task_scheduler.py
```

---

### 3. Ticket Classifier (ticket_classifier.py)

Simulates an automated support ticket pipeline. Messages arrive in a queue and are classified by a keyword-based "AI" before being processed.

**Concepts covered:**
- collections.deque for efficient FIFO operations (O(1))
- Automated classification (Keyword matching)
- Real-world system architecture simulation
- Data tracking with ID, timestamp, and category

**How to run:**
```bash
python3 projects/queues/ticket_classifier.py
```

**Key Advantages:**
- Uses deque instead of list for O(1) removals.
- Separates input (enqueue) from processing (dequeue/classification).
- Demonstrates how to handle streams of unstructured text data.

---

## Project Structure

```
queues/
├── customer_service_sim.py   # Project 1: Customer Service (basic Queue)
├── task_scheduler.py         # Project 2: Task Scheduler (Simple + Priority Queue)
├── ticket_classifier.py      # Project 3: Ticket Classifier (Queue + Keyword Match)
└── README.md                 # This file
```
