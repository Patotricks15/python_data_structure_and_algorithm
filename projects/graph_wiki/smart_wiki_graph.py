import wikipediaapi
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser

# Load environment variables
load_dotenv()

class WikiSmartGraph:
    def __init__(self, user_agent="WikiGraphBot/1.0 (contact: patrick@example.com)", lang='en'):
        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=lang)
        self.graph = nx.DiGraph()
        
        # AI Filter Setup
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            self.parser = CommaSeparatedListOutputParser()
            self.prompt = ChatPromptTemplate.from_template(
                "You are a knowledge graph assistant. Given a topic '{topic}' and a list of related Wikipedia links: {links}. "
                "Pick the top {top_n} most conceptually relevant links to understand '{topic}'. "
                "Return them as a comma-separated list. If the list is empty, return an empty string."
            )
            self.chain = self.prompt | self.llm | self.parser
            print("🤖 AI Filter enabled.")
        else:
            self.llm = None
            print("⚠️ OPENAI_API_KEY not found. AI filtering disabled.")

    def get_smart_links(self, topic, links, top_n=5):
        """Uses LLM to filter the most relevant links."""
        if not self.llm:
            return list(links.keys())[:top_n]
        
        link_titles = list(links.keys())[:20]  # Take a sample to avoid token limits
        try:
            response = self.chain.invoke({"topic": topic, "links": ", ".join(link_titles), "top_n": top_n})
            # Clean response to ensure links exist
            valid_links = [l.strip() for l in response if l.strip() in links]
            return valid_links
        except Exception as e:
            print(f"Error filtering links: {e}")
            return list(links.keys())[:top_n]

    def build_graph(self, start_node, max_depth=2, branch_factor=5):
        """Builds the graph using BFS."""
        queue = deque([(start_node, 0)])
        visited = set([start_node])
        
        print(f"🕸️ Starting graph construction from: {start_node}")
        
        self.graph.add_node(start_node, depth=0)
        
        while queue:
            current_topic, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
                
            page = self.wiki.page(current_topic)
            if not page.exists():
                print(f"❌ Page '{current_topic}' not found on Wikipedia.")
                continue

            print(f"🔍 Exploring: {current_topic} (Depth {depth})")
            
            # Get links and filter them
            all_links = page.links
            relevant_links = self.get_smart_links(current_topic, all_links, top_n=branch_factor)
            
            for link in relevant_links:
                if link not in visited:
                    visited.add(link)
                    self.graph.add_node(link, depth=depth + 1)
                    queue.append((link, depth + 1))
                self.graph.add_edge(current_topic, link)

    def visualize(self):
        """Visualizes the graph using NetworkX and Matplotlib."""
        if not self.graph.nodes():
            print("The graph is empty!")
            return

        plt.figure(figsize=(16, 10))
        
        # Determine color and size based on depth
        depths = [self.graph.nodes[node].get('depth', 2) for node in self.graph.nodes]
        
        # Map depth to color (Darker for root, Lighter for leaves)
        # Using a colormap like 'Blues' or 'GnBu'
        color_map = []
        size_map = []
        for depth in depths:
            if depth == 0:
                color_map.append("#1f77b4") # Dark Blue
                size_map.append(4000)
            elif depth == 1:
                color_map.append("#66b2ff") # Medium Blue
                size_map.append(2500)
            else:
                color_map.append("#cce5ff") # Light Blue
                size_map.append(1000)

        # Better layout for hierarchical structures
        pos = nx.spring_layout(self.graph, k=0.8, iterations=100)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3, edge_color="gray", arrows=True, arrowsize=20)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color=color_map, node_size=size_map)
        
        # Draw labels with slightly larger text for primary and medium for secondary
        labels = {node: node for node in self.graph.nodes}
        for node, depth in nx.get_node_attributes(self.graph, 'depth').items():
            font_size = 12 if depth == 0 else (10 if depth == 1 else 8)
            nx.draw_networkx_labels(self.graph, pos, labels={node: node}, font_size=font_size, font_weight="bold")
        
        plt.title(f"Knowledge Graph: Distinguishing Depth and Relevance", fontsize=16)
        plt.axis('off')
        
        output_path = "projects/graph_wiki/wiki_graph.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        print(f"📊 Visualization saved to {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create a Smart Wikipedia Knowledge Graph")
    parser.add_argument("topic", type=str, help="Starting topic")
    parser.add_argument("--depth", type=int, default=2, help="BFS Depth")
    parser.add_argument("--branch", type=int, default=5, help="Number of links per node")
    
    args = parser.parse_args()
    
    smart_wiki = WikiSmartGraph()
    smart_wiki.build_graph(args.topic, max_depth=args.depth, branch_factor=args.branch)
    
    print(f"\n✅ Graph built with {len(smart_wiki.graph.nodes)} nodes and {len(smart_wiki.graph.edges)} edges.")
    smart_wiki.visualize()
