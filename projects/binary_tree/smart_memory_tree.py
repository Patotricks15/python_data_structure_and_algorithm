import os
import uuid
import spacy
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from .env
load_dotenv()

@dataclass
class MemoryNode:
    """Memory Node for Binary Search Tree."""
    importance: float
    content: str
    role: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    left: Optional['MemoryNode'] = field(default=None, repr=False)
    right: Optional['MemoryNode'] = field(default=None, repr=False)

class SmartMemoryTree:
    """BST Memory Manager."""
    def __init__(self):
        self.root: Optional[MemoryNode] = None
        self.size: int = 0

    def insert(self, role: str, content: str, importance: float):
        """Inserts a new memory based on its importance score. O(log n)."""
        new_node = MemoryNode(role=role, content=content, importance=importance)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)
        self.size += 1

    def _insert_recursive(self, current: MemoryNode, new_node: MemoryNode):
        if new_node.importance < current.importance:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursive(current.right, new_node)

    def get_most_important(self, limit: int = 5) -> str:
        """Retrieves the most important memories formatted as context string (Reverse In-order)."""
        memories = []
        self._reverse_inorder(self.root, memories, limit)
        
        context = ""
        for m in memories:
            context += f"{m['role'].upper()}: {m['content']}\n"
        return context

    def _reverse_inorder(self, node: Optional[MemoryNode], memories: List[Dict], limit: int):
        if node is None or len(memories) >= limit:
            return
        self._reverse_inorder(node.right, memories, limit)
        if len(memories) < limit:
            memories.append({
                "importance": node.importance,
                "role": node.role,
                "content": node.content
            })
        self._reverse_inorder(node.left, memories, limit)

    def get_high_importance_memories(self, threshold: float = 7.0) -> List[str]:
        """Retrieves all memories with importance above a certain threshold."""
        high_val_memories = []
        self._collect_high_importance(self.root, threshold, high_val_memories)
        return high_val_memories

    def _collect_high_importance(self, node: Optional[MemoryNode], threshold: float, results: List[str]):
        if node:
            self._collect_high_importance(node.left, threshold, results)
            if node.importance >= threshold:
                results.append(f"[{node.role.upper()}]: {node.content}")
            self._collect_high_importance(node.right, threshold, results)

    def display_tree(self):
        """Prints an ASCII representation of the tree for visualization."""
        if not self.root:
            print("Memory tree is empty.")
            return
        print("\n--- Memory Structure Visualization (BST) ---")
        self._print_recursive(self.root, "", True)

    def _print_recursive(self, node: Optional[MemoryNode], indent: str, last: bool):
        if node:
            print(indent, end="")
            if last:
                print("└── ", end="")
                indent += "    "
            else:
                print("├── ", end="")
                indent += "│   "
            
            # Node format: [Score] Role: Content (truncated)
            content_preview = (node.content[:30] + "..") if len(node.content) > 30 else node.content
            print(f"[{node.importance}] {node.role.upper()}: {content_preview}")
            
            # Recurse: Right then Left for logical terminal view
            self._print_recursive(node.right, indent, False)
            self._print_recursive(node.left, indent, True)

class AI_Brain:
    def __init__(self):
        self.memory = SmartMemoryTree()
        # Using a reliable model for importance scoring
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
        self.last_ai_response = "No conversation started yet."
        
        # Load SpaCy Portuguese model for NER (Named Entity Recognition)
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except Exception:
            # Fallback if model is not found
            self.nlp = None

        # Scorer prompt with context and strict rules
        self.scorer_prompt = ChatPromptTemplate.from_template(
            "You are a long-term memory relevance classifier for an AI.\n"
            "Evaluate the IMPORTANCE of the USER's last message (0.0 to 10.0) to be remembered in FUTURE conversations.\n\n"
            "CONTEXT (AI's last message): {context}\n"
            "USER MESSAGE: {message}\n\n"
            "NOTING GUIDE:\n"
            "- 9.5-10.0: CRITICAL DATA (Names, keys, addresses, unique vital life facts).\n"
            "- 7.5-9.0: PERSISTENT PREFERENCES (Specific tastes, allergies, recurring real-life habits).\n"
            "- 4.0-7.0: CURRENT TASK CONTEXT (What the user wants to do now, project details).\n"
            "- 1.5-3.5: GENERAL CURIOSITY / KNOWLEDGE (Questions about world facts like 'types of cheese' are NOT about the user).\n"
            "- 0.0-1.4: SMALL TALK / GREETINGS ('Hi', 'How are you?', 'Cool', 'Kkk').\n\n"
            "TIP: If the message is a general knowledge question, give it a LOW score. High scores are only for things UNIQUE to the user.\n\n"
            "Respond ONLY with the decimal number."
        )
        
        # Main chat prompt
        self.chat_prompt = ChatPromptTemplate.from_template(
            "You are a smart assistant. Use the important memories context below to answer the user.\n\n"
            "RELEVANT MEMORIES CONTEXT:\n{context}\n\n"
            "USER: {input}\nASSISTENTE:"
        )

    def _get_ner_score(self, text: str) -> float:
        """Determines importance based on the number of detected entities (Names, Dates, Locations)."""
        if not self.nlp:
            return 0.0
        
        doc = self.nlp(text)
        entities = doc.ents
        # Each entity counts for 2.5 points, capped at 10.0
        ner_score = len(entities) * 2.5
        return min(ner_score, 10.0)

    def _get_importance_score(self, text: str) -> float:
        """Hybrid approach: Max of LLM judgment and NER entity detection."""
        # 1. Get score from LLM (Subjective/Contextual)
        llm_score = 1.0
        try:
            chain = self.scorer_prompt | self.llm | StrOutputParser()
            score_str = chain.invoke({"message": text, "context": self.last_ai_response})
            llm_score = float(score_str.strip())
        except Exception:
            llm_score = 3.0 # Fallback 

        # 2. Get score from NER (Objective/Factual)
        ner_score = self._get_ner_score(text)
        
        # 3. Final score is the maximum of both worlds
        final_score = max(llm_score, ner_score)
        print(f"[Internal] LLM Score: {llm_score} | NER Score: {ner_score}")
        
        return min(final_score, 10.0)

    def chat(self, user_input: str):
        # 1. Evaluate importance considering latest AI context
        score = self._get_importance_score(user_input)
        print(f"[System] Detected Importance: {score}/10.0")
        
        # 2. Retrieve Top-K context from the BST
        memory_context = self.memory.get_most_important(limit=3)
        
        # 3. Generate response using context
        chain = self.chat_prompt | self.llm | StrOutputParser()
        response = chain.invoke({"context": memory_context, "input": user_input})
        
        # 4. Save both input and AI response into the Tree
        self.memory.insert("user", user_input, score)
        
        # Update trackers
        self.last_ai_response = response
        
        # AI responses usually have neutral/low-task importance
        self.memory.insert("assistant", response, 3.0)
        
        return response

    def generate_final_summary(self):
        """Generates a summary using only high-importance memories (score >= 7.0)."""
        high_val_memories = self.memory.get_high_importance_memories(threshold=7.0)
        
        if not high_val_memories:
            return "No highly important information was shared during this session."
        
        context_str = "\n".join(high_val_memories)
        
        summary_prompt = ChatPromptTemplate.from_template(
            "Based on these high-importance memories from the binary tree, "
            "generate a concise summary of what we learned about the user and their main goals:\n\n"
            "{memories}\n\nSUMMARY:"
        )
        
        chain = summary_prompt | self.llm | StrOutputParser()
        return chain.invoke({"memories": context_str})

# --- CLI Chat Loop ---
if __name__ == "__main__":
    brain = AI_Brain()
    print("🤖 AI Brain with Hybrid Memory Active! (Type 'exit' to end and see summary)")
    
    while True:
        try:
            user_msg = input("\nYou: ")
            if user_msg.lower().strip() == "exit":
                break
                
            ai_response = brain.chat(user_msg)
            print(f"Assistant: {ai_response}")
        except KeyboardInterrupt:
            break
            
    print("\n--- Generating Session Summary from High-Importance Nodes (>= 7.0) ---")
    summary = brain.generate_final_summary()
    print(summary)
        
    print("\n--- Final Memory Tree Report ---")
    brain.memory.display_tree()
    print("\n--------------------------------")
