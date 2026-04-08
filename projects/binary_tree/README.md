# 🌳 Gen AI Smart Memory (Binary Search Tree + LangChain + NLP)

This project demonstrates how a **Binary Search Tree (BST)** can be used to manage AI assistant memory more intelligently than a simple linear history. It combines classical data structures with modern LLM capabilities and deterministic NLP.

## 🚀 Key Features

-   **Hybrid Importance Scoring**: Uses a dual-judge system to evaluate every message:
    -   **Subjective (LLM)**: Analyzes semantic context and user preferences using LangChain.
    -   **Objective (NER)**: Uses SpaCy to detect named entities (Names, Dates, Locations), ensuring factual data is always prioritized.
-   **BST-Based Organization**: Memories are stored in a Binary Search Tree using the importance score as the **Key**. This allows for $O(\log n)$ search and organized ranking.
-   **Smart Retrieval**: Performer **Reverse In-order Traversal** to inject the Top-K most relevant memories into the AI's current context window.
-   **Automatic Summarization**: Upon typing `exit`, the system retrieves all high-value nodes (score $\ge 7.0$) and generates a concise **User Profile Summary**.
-   **ASCII Visualization**: Prints a visual representation of the tree structure at the end of every session.

## 🛠️ Tech Stack
-   **LangChain**: Prompt orchestration and LLM chains.
-   **OpenAI (GPT-3.5-Turbo-1106)**: For conversational logic and importance scoring.
-   **SpaCy (pt_core_news_sm)**: For deterministic Named Entity Recognition.
-   **Python Dotenv**: Secure environment variable management.

## ⚖️ Importance Scoring Scale
The hybrid scorer follows a strict hierarchy to ensure memory efficiency:
-   **9.5 - 10.0**: CRITICAL DATA (Unique personal info, security keys, vital facts).
-   **7.5 - 9.0**: PERSISTENT PREFERENCES (Tastes, hobbies, core lifestyle habits).
-   **4.0 - 7.0**: TASK CONTEXT (Details about the current conversation goals).
-   **Below 4.0**: GENERAL CURIOSITY / SMALL TALK (Greetings, world facts, jokes).

## 💻 How to Run

1. **Set up your environment**:
   Create a `.env` file in the root directory with your `OPENAI_API_KEY`.

2. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Smart Chat**:
   ```bash
   python projects/binary_tree/smart_memory_tree.py
   ```
   *Type `exit` to end the session and see the final summary and tree structure.*

## 🧠 Why use Trees?
In a standard chat list, finding the most important items takes $O(n)$. In a balanced Binary Search Tree, we maintain an organized memory and extract priority context in $O(\log n)$ time. This architecture bridges the gap between simple chat history and complex Vector Databases.
