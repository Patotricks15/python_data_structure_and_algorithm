from dataclasses import dataclass


# ============================================================
# STEP 1: The Stack Class
# A Stack follows the LIFO rule: Last In, First Out.
#
# Imagine a stack of books:
# - You always ADD a book on TOP (push)
# - You always REMOVE from the TOP (pop)
# - The LAST book placed is the FIRST one you can grab
#
# This is the exact opposite of a Queue!
# ============================================================

class Stack:
    def __init__(self, max_size=10):
        self.items = []
        # Max size limits how many undo/redo actions we keep.
        # If we go over the limit, the oldest action is removed.
        self.max_size = max_size

    def is_empty(self):
        """Returns True if the stack has no items."""
        return len(self.items) == 0

    def push(self, item):
        """
        Adds an item to the TOP of the stack.
        If we hit the max size, we remove the OLDEST action (bottom).
        """
        if len(self.items) >= self.max_size:
            self.items.pop(0)  # Remove the oldest entry from the bottom
        self.items.append(item)

    def pop(self):
        """
        Removes and returns the item from the TOP of the stack.
        pop() with no arguments always removes the last item (the top).
        This is what makes it a Stack and not a Queue!
        """
        if not self.is_empty():
            return self.items.pop()  # No index = removes from the END (top)
        return None

    def peek(self):
        """Look at the top item without removing it."""
        if not self.is_empty():
            return self.items[-1]  # -1 is the last index = the top
        return None

    def size(self):
        return len(self.items)

    def display(self):
        """
        Shows the stack from TOP to BOTTOM.
        The first item shown is the one that would be popped next.
        """
        if self.is_empty():
            return "(empty)"
        # Reverse the list so the TOP (last item) is shown first
        return " | ".join([f"'{a.description}'" for a in reversed(self.items)])


# ============================================================
# STEP 2: The Action Dataclass
# Represents a single action the user performed in the editor.
# We store a SNAPSHOT of the document BEFORE the action happened.
# This is what lets us travel back in time with Undo!
# ============================================================

@dataclass
class Action:
    description: str  # A human-readable label, e.g. "Wrote: 'Hello'"
    snapshot: str     # The document content BEFORE this action was done


# ============================================================
# STEP 3: The Text Editor
# A simple document that supports write and delete.
# Every change is saved as an Action on the undo stack.
# ============================================================

class TextEditor:
    def __init__(self):
        self.document = ""              # The current text content
        self.undo_stack = Stack(max_size=10)  # History of actions (up to 10)
        self.redo_stack = Stack(max_size=10)  # Actions that were undone

    def write(self, text):
        """
        Appends text to the document.
        Before changing anything, we save the current state to the undo stack.
        """
        # Save the state BEFORE the change so we can restore it on undo
        action = Action(
            description=f"Wrote: '{text}'",
            snapshot=self.document      # Save what the document looks like NOW
        )
        self.undo_stack.push(action)

        # Also clear the redo stack — once you do a new action,
        # the old redo history no longer makes sense.
        self.redo_stack = Stack(max_size=10)

        # Now apply the change
        self.document += text
        print(f"  ✏️  Wrote: '{text}'")

    def delete_last_word(self):
        """
        Removes the last word from the document.
        Works the same as write: save state first, then apply.
        """
        if not self.document.strip():
            print("  ❌ Nothing to delete.")
            return

        words = self.document.split(" ")
        last_word = words[-1]

        action = Action(
            description=f"Deleted: '{last_word}'",
            snapshot=self.document
        )
        self.undo_stack.push(action)
        self.redo_stack = Stack(max_size=10)

        # Remove last word
        self.document = " ".join(words[:-1])
        print(f"  🗑️  Deleted last word: '{last_word}'")

    def undo(self):
        """
        Reverts the last action.

        How it works:
        1. Pop the last action from the UNDO stack
        2. Save the CURRENT state to the REDO stack (so we can redo later)
        3. Restore the document to the snapshot saved in the action
        """
        if self.undo_stack.is_empty():
            print("  ❌ Nothing to undo.")
            return

        # Take the last action off the undo stack
        last_action = self.undo_stack.pop()

        # Save current state to redo stack so we can go forward again
        redo_action = Action(
            description=f"Redo: '{last_action.description}'",
            snapshot=self.document      # Current state before undoing
        )
        self.redo_stack.push(redo_action)

        # Restore the document to what it was BEFORE that action
        self.document = last_action.snapshot
        print(f"  ↩️  Undid: {last_action.description}")

    def redo(self):
        """
        Re-applies an action that was undone.

        How it works:
        1. Pop from the REDO stack
        2. Save to the UNDO stack (so we can undo again if needed)
        3. Restore the document to the snapshot saved in the redo action
        """
        if self.redo_stack.is_empty():
            print("  ❌ Nothing to redo.")
            return

        redo_action = self.redo_stack.pop()

        # Save current state back to undo stack
        undo_action = Action(
            description=f"Undo: '{redo_action.description}'",
            snapshot=self.document
        )
        self.undo_stack.push(undo_action)

        # Restore the document
        self.document = redo_action.snapshot
        print(f"  ↪️  Redid: {redo_action.description}")

    def show(self):
        """Display the current content of the document."""
        print(f"\n  📄 Document: \"{self.document}\"")

    def history(self):
        """Show the current undo and redo stacks."""
        print(f"\n  --- ACTION HISTORY ---")
        print(f"  Undo stack (top → bottom): {self.undo_stack.display()}")
        print(f"  Redo stack (top → bottom): {self.redo_stack.display()}")
        print(f"  Max history: {self.undo_stack.max_size} actions")


# ============================================================
# STEP 4: The Interactive Simulator
# ============================================================

def main():
    editor = TextEditor()

    print("\n" + "=" * 50)
    print("        SIMPLE TEXT EDITOR")
    print("        (Undo / Redo with Stacks)")
    print("=" * 50)
    print("Commands:")
    print("  write <text>  -> Add text to the document")
    print("  delete        -> Remove the last word")
    print("  undo          -> Undo last action  (Ctrl+Z)")
    print("  redo          -> Redo last action  (Ctrl+Y)")
    print("  show          -> Show the document")
    print("  history       -> Show undo/redo stacks")
    print("  exit          -> Quit the editor")
    print("=" * 50)
    editor.show()

    while True:
        try:
            user_input = input("\n> Command: ").strip()

            if not user_input:
                continue

            # Split input into command and optional argument
            parts = user_input.split(" ", 1)
            command = parts[0].lower()
            argument = parts[1] if len(parts) > 1 else ""

            if command == "write":
                if not argument:
                    print("  ⚠️  Usage: write <your text here>")
                else:
                    editor.write(" " + argument if editor.document else argument)
                    editor.show()

            elif command == "delete":
                editor.delete_last_word()
                editor.show()

            elif command == "undo":
                editor.undo()
                editor.show()

            elif command == "redo":
                editor.redo()
                editor.show()

            elif command == "show":
                editor.show()

            elif command == "history":
                editor.history()

            elif command == "exit":
                print("\n  Editor closed. Goodbye! 👋")
                break

            else:
                print("  ⚠️  Unknown command. Use: write, delete, undo, redo, show, history, or exit.")

        except KeyboardInterrupt:
            print("\n\n  Interrupted. Closing editor...")
            break


if __name__ == "__main__":
    main()
