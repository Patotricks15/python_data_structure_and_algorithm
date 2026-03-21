# Queues — Practical Projects

This folder contains practical projects built using the **Queue** data structure in Python.

---

## What is a Queue?

A **Queue** follows the **FIFO** rule:

> **F**irst **I**n, **F**irst **O**ut

Think of a real-life line at a coffee shop:
- The **first person to arrive** is the **first person to be served**.
- New people always join at the **back** of the line.
- The attendant always serves from the **front** of the line.

### Key Operations

| Operation  | What it does                              | Method used    |
|------------|-------------------------------------------|----------------|
| `enqueue`  | Adds an item to the **back** of the queue | `append(item)` |
| `dequeue`  | Removes item from the **front**           | `pop(0)`       |
| `peek`     | Looks at the front item (no removal)      | `items[0]`     |
| `is_empty` | Checks if the queue has no items          | `len() == 0`   |

### Visual Diagram

```
BACK (new arrivals)              FRONT (served next)
       |                               |
  [Carlos] -> [Bob] -> [Ana]  --->  served!
```

---

## Projects

### 1. Customer Service Simulator (`customer_service_sim.py`)

Simulates a support desk where customers arrive and wait in line to be served.

**Concepts covered:**
- Basic `Queue` class (FIFO logic)
- `@dataclass` for the `Customer` model
- `enqueue` / `dequeue` / `peek` / `display`
- Interactive terminal menu

**How to run:**
```bash
python3 queues/customer_service_sim.py
```

**Available commands:**

| Command  | Action                              |
|----------|-------------------------------------|
| `add`    | Add a new customer to the line      |
| `serve`  | Serve the next customer in line     |
| `status` | Show the current state of the line  |
| `exit`   | Close the simulator                 |

---

### 2. Task Scheduler (`task_scheduler.py`)

Simulates how an operating system or web server handles background tasks.
Implements **two types of queues** side by side so you can compare them.

**Concepts covered:**
- `SimpleQueue` — basic FIFO (tasks run in arrival order)
- `PriorityQueue` — uses Python's `heapq` (most urgent tasks run first)
- `@dataclass` for the `Task` model
- Priority levels: `HIGH (1)`, `MEDIUM (2)`, `LOW (3)`

**How `heapq` works:**

`heapq` is a **min-heap**: the smallest value always stays at the top.
Since `HIGH = 1` is the smallest, it always gets processed first.

Tasks are stored as tuples `(priority, counter, task)`:
- `priority` → determines urgency
- `counter` → tiebreaker (FIFO within the same priority level)

**How to run:**
```bash
python3 queues/task_scheduler.py
```

**Available commands:**

| Command  | Action                                                  |
|----------|---------------------------------------------------------|
| `add`    | Add a new task with name, description, priority, duration |
| `run`    | Process the next task (choose Simple or Priority Queue) |
| `status` | Show the state of both queues                           |
| `exit`   | Close the simulator                                     |

---

## Project Structure

```
queues/
├── customer_service_sim.py   # Project 1: Customer Service (basic Queue)
├── task_scheduler.py         # Project 2: Task Scheduler (Simple + Priority Queue)
└── README.md                 # This file
```
