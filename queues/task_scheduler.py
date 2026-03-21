import time
import heapq
from dataclasses import dataclass, field


# ============================================================
# PRIORITY LEVELS
# We use constants so the code is more readable.
# Instead of writing 1, 2, 3 everywhere, we write HIGH, MEDIUM, LOW.
# ============================================================

HIGH   = 1
MEDIUM = 2
LOW    = 3

PRIORITY_LABELS = {
    HIGH:   "🔴 HIGH",
    MEDIUM: "🟡 MEDIUM",
    LOW:    "🟢 LOW",
}


# ============================================================
# STEP 1: The Task Dataclass
# Represents a background task (like an OS job or server task).
# ============================================================

@dataclass
class Task:
    name: str          # Name of the task (e.g. "Database Backup")
    description: str   # What the task does
    priority: int      # 1 = HIGH, 2 = MEDIUM, 3 = LOW
    duration: int      # How many seconds it takes to complete

    def __str__(self):
        label = PRIORITY_LABELS.get(self.priority, "UNKNOWN")
        return (
            f"Task: '{self.name}' | "
            f"Priority: {label} | "
            f"Duration: {self.duration}s | "
            f"Info: {self.description}"
        )


# ============================================================
# STEP 2: Simple Queue (FIFO)
# Tasks are processed in the order they were added.
# No priorities — first in, first out.
# ============================================================

class SimpleQueue:
    """
    A basic FIFO queue.
    Tasks are processed in the exact order they arrive.
    """
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, task):
        """Add task to the back of the line."""
        self.items.append(task)

    def dequeue(self):
        """Remove and return the task from the front."""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def size(self):
        return len(self.items)

    def display(self):
        if self.is_empty():
            return "(no tasks in queue)"
        return " -> ".join([f"[{t.name}]" for t in self.items])


# ============================================================
# STEP 3: Priority Queue
# Uses Python's heapq module (a min-heap).
#
# How it works:
# - heapq always keeps the SMALLEST value at the top.
# - We store tasks as tuples: (priority_number, counter, task)
# - Since HIGH = 1, MEDIUM = 2, LOW = 3...
#   the smallest number = the most urgent task!
# - The counter is a tiebreaker: if two tasks have the same
#   priority, the one added first is processed first (FIFO).
# ============================================================

class PriorityQueue:
    """
    A Priority Queue using heapq (min-heap).
    HIGH priority tasks (value=1) are always processed before
    MEDIUM (value=2) and LOW (value=3) tasks.
    """
    def __init__(self):
        self.heap = []          # Internal storage (a heap, not a regular list!)
        self._counter = 0       # Tiebreaker: ensures FIFO for equal priorities

    def is_empty(self):
        return len(self.heap) == 0

    def enqueue(self, task):
        """
        Push a task into the heap.
        The tuple (priority, counter, task) is what heapq uses to sort.
        Python compares tuples left-to-right:
          first by priority, then by counter (if priorities are equal).
        """
        entry = (task.priority, self._counter, task)
        heapq.heappush(self.heap, entry)
        self._counter += 1

    def dequeue(self):
        """
        Pop the task with the HIGHEST priority (lowest number).
        heappop() always removes the smallest element from the heap.
        """
        if not self.is_empty():
            priority, counter, task = heapq.heappop(self.heap)
            return task
        return None

    def peek(self):
        """See the next task without removing it."""
        if not self.is_empty():
            priority, counter, task = self.heap[0]
            return task
        return None

    def size(self):
        return len(self.heap)

    def display(self):
        if self.is_empty():
            return "(no tasks in queue)"
        # Sort a copy to show in priority order (heap order is not always sorted visually)
        sorted_tasks = sorted(self.heap)
        return " -> ".join([f"[{t.name}({PRIORITY_LABELS[t.priority]})]" for _, _, t in sorted_tasks])


# ============================================================
# STEP 4: The Worker
# This function simulates a worker that processes tasks.
# ============================================================

def process_task(task):
    """Simulates a worker processing a task."""
    print(f"\n  ⚙️  Starting task: {task.name}")
    print(f"  📋 Details      : {task.description}")
    print(f"  ⏳ Processing   : ", end="", flush=True)

    # Simulate the task running step by step
    for _ in range(task.duration):
        time.sleep(0.5)
        print("█", end="", flush=True)

    print(f"\n  ✅ Task '{task.name}' completed!\n")


# ============================================================
# STEP 5: The Interactive Simulator
# ============================================================

def get_priority_input():
    """Helper to get a valid priority from the user."""
    while True:
        print("  Priority options: 1=HIGH  2=MEDIUM  3=LOW")
        choice = input("  Choose priority (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print("  ❌ Invalid option. Enter 1, 2, or 3.")


def main():
    simple_queue   = SimpleQueue()
    priority_queue = PriorityQueue()

    print("\n" + "=" * 50)
    print("        TASK SCHEDULER SIMULATOR")
    print("        (Simple Queue + Priority Queue)")
    print("=" * 50)
    print("Commands: add | run | status | exit")
    print("=" * 50)

    while True:
        try:
            action = input("\n> Enter command: ").lower().strip()

            # --------------------------------------------------
            # ADD: Create a new task and add it to both queues
            # --------------------------------------------------
            if action == "add":
                print("\n  -- New Task --")
                name        = input("  Task name (e.g. Database Backup): ")
                description = input("  Description (e.g. Back up all user data): ")
                priority    = get_priority_input()
                duration    = int(input("  Duration in seconds (1-5): "))

                new_task = Task(name, description, priority, duration)

                simple_queue.enqueue(new_task)
                priority_queue.enqueue(new_task)

                print(f"\n  ✅ Task '{name}' added to both queues!")
                print(f"     {PRIORITY_LABELS[priority]} priority")

            # --------------------------------------------------
            # RUN: Process the next task (choose which queue)
            # --------------------------------------------------
            elif action == "run":
                if simple_queue.is_empty():
                    print("  ❌ No tasks to process.")
                else:
                    print("\n  Which queue should process the next task?")
                    print("  1 -> Simple Queue (FIFO — first added is first served)")
                    print("  2 -> Priority Queue (most urgent goes first)")
                    mode = input("  Choose (1/2): ").strip()

                    if mode == "1":
                        task = simple_queue.dequeue()
                        priority_queue.dequeue()  # Keep both queues in sync
                        print(f"\n  [SIMPLE QUEUE] Processing: {task.name}")
                        process_task(task)

                    elif mode == "2":
                        task = priority_queue.dequeue()
                        # Remove the same task from simple_queue to keep in sync
                        simple_queue.items = [t for t in simple_queue.items if t.name != task.name]
                        print(f"\n  [PRIORITY QUEUE] Processing: {task.name}")
                        process_task(task)
                    else:
                        print("  ❌ Invalid choice.")

            # --------------------------------------------------
            # STATUS: Display the state of both queues
            # --------------------------------------------------
            elif action == "status":
                print("\n  --- QUEUE STATUS ---")
                print(f"  Total tasks in queue : {simple_queue.size()}")
                print(f"\n  📋 Simple Queue (FIFO order):")
                print(f"     {simple_queue.display()}")
                print(f"\n  ⚡ Priority Queue (by urgency):")
                print(f"     {priority_queue.display()}")
                if not priority_queue.is_empty():
                    next_task = priority_queue.peek()
                    print(f"\n  👀 Next by priority  : [{next_task.name}] ({PRIORITY_LABELS[next_task.priority]})")

            # --------------------------------------------------
            # EXIT
            # --------------------------------------------------
            elif action == "exit":
                print("\n  Scheduler shutting down. Goodbye! 👋")
                break

            else:
                print("  ⚠️  Unknown command. Use: add, run, status, or exit.")

        except KeyboardInterrupt:
            print("\n\n  Interrupted. Shutting down...")
            break
        except ValueError:
            print("  ❌ Please enter a valid number.")


if __name__ == "__main__":
    main()
