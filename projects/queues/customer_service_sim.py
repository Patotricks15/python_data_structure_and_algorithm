import time
from dataclasses import dataclass


# ============================================================
# STEP 1: The Queue Class
# This is our "waiting line" engine.
# It follows the FIFO rule: First In, First Out.
# Like a bus stop: the first person to arrive is the first to board.
# ============================================================

class Queue:
    def __init__(self):
        # We use a simple list to store the customers
        self.items = []

    def is_empty(self):
        """Returns True if there is nobody in line."""
        return len(self.items) == 0

    def enqueue(self, item):
        """
        Adds a customer to the BACK of the line.
        append() always adds to the end of the list.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the customer from the FRONT of the line.
        pop(0) removes the item at index 0 (the first one).
        This is what makes it a Queue and not a Stack!
        """
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        """Look at who is next WITHOUT removing them from the line."""
        if not self.is_empty():
            return self.items[0]
        return None

    def size(self):
        """Returns the total number of people waiting."""
        return len(self.items)

    def display(self):
        """
        Shows the line visually.
        Example: [Ana] -> [Bob] -> [Carlos]
        The LEFT side is the FRONT (served next).
        The RIGHT side is the BACK (arrived last).
        """
        if self.is_empty():
            return "(empty line)"
        return " -> ".join([f"[{c.name}]" for c in self.items])


# ============================================================
# STEP 2: The Customer Class
# Using @dataclass: Python automatically generates __init__
# and __repr__ for us — no need to write them manually!
# ============================================================

@dataclass
class Customer:
    name: str   # The customer's name
    issue: str  # The reason for their visit

    def __str__(self):
        # We define __str__ to control how it looks when printed
        return f"Customer: {self.name} | Issue: {self.issue}"


# ============================================================
# STEP 3: The Simulator
# This is the interactive part where everything comes together.
# ============================================================

def main():
    service_queue = Queue()

    print("\n" + "=" * 45)
    print("      CUSTOMER SERVICE SIMULATOR")
    print("      (Queue / FIFO Data Structure)")
    print("=" * 45)
    print("Available commands:")
    print("  add    -> Add a new customer to the line")
    print("  serve  -> Serve the next customer in line")
    print("  status -> See the current state of the line")
    print("  exit   -> Close the simulator")
    print("=" * 45)

    while True:
        try:
            action = input("\n> Enter command: ").lower().strip()

            # --- ADD a customer to the queue ---
            if action == "add":
                name = input("  Customer name: ")
                issue = input("  Reason for visit: ")
                new_customer = Customer(name, issue)
                service_queue.enqueue(new_customer)
                print(f"  ✅ {name} has joined the line. Position: #{service_queue.size()}")

            # --- SERVE the next customer ---
            elif action == "serve":
                if service_queue.is_empty():
                    print("  ❌ No one is waiting in line right now.")
                else:
                    customer = service_queue.dequeue()
                    print(f"\n  🔔 Now serving: {customer}")
                    print("  ⏳ Processing request, please wait...")
                    time.sleep(1.5)  # Simulates the time it takes to help a customer
                    print(f"  ✅ Done! {customer.name}'s issue has been resolved.")
                    print(f"  📋 Remaining in line: {service_queue.size()} person(s)")

            # --- STATUS of the queue ---
            elif action == "status":
                print("\n  --- QUEUE STATUS ---")
                print(f"  Total waiting : {service_queue.size()} person(s)")
                print(f"  Line view     : {service_queue.display()}")
                if not service_queue.is_empty():
                    next_up = service_queue.peek()
                    print(f"  Next to serve : {next_up.name}")
                    estimated_wait = service_queue.size() * 5
                    print(f"  Estimated wait: ~{estimated_wait} minutes")

            # --- EXIT ---
            elif action == "exit":
                print("\n  Shutting down the simulator. Goodbye! 👋")
                break

            else:
                print("  ⚠️  Unknown command. Use: add, serve, status, or exit.")

        except KeyboardInterrupt:
            print("\n\n  Interrupted. Shutting down...")
            break


# This block only runs when you execute this file directly.
# If another file imports this one, it will NOT run automatically.
if __name__ == "__main__":
    main()
