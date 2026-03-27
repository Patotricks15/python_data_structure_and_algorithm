import heapq
from dataclasses import dataclass, field
from datetime import datetime
import time
from typing import Optional, Dict

@dataclass(order=True)
class Ticket:
    """
    Represents a support ticket.
    The 'order=True' allows the heap to sort tickets by priority automatically.
    """
    priority: int      # 1: Urgent, 2: Normal, 3: Low
    id: int = field(compare=False)
    message: str = field(compare=False)
    timestamp: datetime = field(default_factory=datetime.now, compare=False)

class TicketSystem:
    """
    Advanced Ticket System using a Priority Queue (heapq).
    Automatically classifies priority based on message content.
    """
    def __init__(self):
        # Using a list as a heap (Priority Queue)
        self.queue = []
        self.ticket_counter = 1

    def _classify_priority(self, message: str) -> int:
        """
        Determines the priority level based on keywords.
        1 = HIGH (Urgent), 2 = MEDIUM (Normal), 3 = LOW
        """
        m = message.lower()
        
        # Priority 1: Critical issues
        if any(word in m for word in ["crash", "broken", "critical", "urgent", "error", "bug"]):
            return 1
        
        # Priority 2: Business/Financial issues
        if any(word in m for word in ["cancel", "price", "payment", "subscription", "fail"]):
            return 2
        
        # Priority 3: Everything else
        return 3

    def add_ticket(self, message: str):
        """Classifies the message and pushes it to the Priority Queue."""
        priority = self._classify_priority(message)
        new_ticket = Ticket(priority=priority, id=self.ticket_counter, message=message)
        
        # Push to heap: O(log n)
        heapq.heappush(self.queue, new_ticket)
        
        priority_label = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}[priority]
        print(f"[INPUT] Ticket #{self.ticket_counter} received (Priority: {priority_label}): '{message}'")
        
        self.ticket_counter += 1

    def process_next(self) -> Optional[Dict]:
        """Processes the highest priority ticket (the lowest priority value)."""
        if not self.queue:
            print("[EMPTY] No tickets to process.")
            return None

        # Pop from heap: O(log n) - always gets the lowest 'priority' number (highest urgency)
        ticket = heapq.heappop(self.queue)
        
        priority_label = {1: "HIGH", 2: "MEDIUM", 3: "LOW"}[ticket.priority]
        print(f"[PROCESS] Processing Ticket #{ticket.id} ({priority_label} priority)...")
        time.sleep(0.5)
        
        return {
            "id": ticket.id,
            "message": ticket.message,
            "priority": priority_label,
            "timestamp": ticket.timestamp.strftime("%H:%M:%S")
        }

# --- Demo ---
if __name__ == "__main__":
    system = TicketSystem()

    # Incoming tickets (various orders)
    print("--- RECEIVING TICKETS ---")
    system.add_ticket("Just saying hi!")                          # Low (3)
    system.add_ticket("The login page is CRASHED and broken!")    # High (1)
    system.add_ticket("I want to cancel my subscription.")        # Medium (2)
    system.add_ticket("There is a bug in the settings.")          # High (1)
    print("-" * 30 + "\n")

    # Processing (should follow High -> Medium -> Low regardless of arrival time)
    print("--- PROCESSING PRIORITY QUEUE ---")
    while system.queue:
        result = system.process_next()
        print(f"Result: [{result['priority']}] ID: {result['id']} | Message: {result['message']}\n")
    
    print("All tickets handled by priority.")
