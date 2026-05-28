# 🕸️ AI-Powered Wiki Knowledge Graph

This project demonstrates the use of **Graph Data Structures** and **Breadth-First Search (BFS)** to build a dynamic knowledge map from Wikipedia. It uses an optional AI layer to filter relevant links, ensuring the graph remains focused on the core subject.

## 🚀 Key Features

-   **BFS Traversal**: Explores Wikipedia topics level by level, starting from a root keyword.
-   **Graph Representation**: Uses `NetworkX` to manage nodes (topics) and edges (relationships).
-   **AI Relevance Filter**: Integrates `LangChain` and `GPT-3.5` to analyze links and select only the most conceptually relevant ones for the graph.
-   **Dynamic Visualization**: Generates a visual map of the connections using `Matplotlib`.
-   **Lazy Loading**: Instead of scraping the whole Wikipedia, it constructs the graph on-the-fly based on your interests.

## 🛠️ Tech Stack

-   **Wikipedia-API**: For fetching page data and links.
-   **NetworkX**: Core library for graph data structures and algorithms.
-   **Matplotlib**: For rendering the graph map.
-   **LangChain & OpenAI**: For the semantic filtering engine.
-   **Python Dotenv**: Environment variable management for API keys.

## 🧠 Concepts Applied

1.  **Directed Graphs**: Connections are directed (Page A links to Page B).
2.  **Breadth-First Search (BFS)**: Ideal for discovering neighbors in a social or knowledge network.
3.  **Adjacency Management**: Efficiently storing and navigating node relationships.
4.  **Semantic Filtering**: Using LLMs to prune the graph, solving the "noise" problem in large-scale data structures.

## 💻 How to Run

1.  **Set up your environment**:
    Ensure your `.env` file has your `OPENAI_API_KEY`. (The project will work without it but will use the first few links found instead of smart filtering).

2.  **Activate the Virtual Environment**:
    ```bash
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install Wikipedia-API networkx matplotlib langchain langchain-openai python-dotenv
    ```

4.  **Run the Generator**:
    ```bash
    python projects/graph_wiki/smart_wiki_graph.py "Linear regression" --depth 2 --branch 5
    ```

## 📊 Example Visualization

When you run the script for "Linear regression", it will:
1.  Fetch the "Linear regression" page.
2.  Ask the AI: "Which of these links are most important to understand Linear Regression?".
3.  Add nodes for "Least squares", "Statistics", "Normal distribution", etc.
4.  Repeat for those nodes until the specified depth.
5.  Render a directed graph of the knowledge cluster.
