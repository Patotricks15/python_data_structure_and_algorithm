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

class TopicNode:
    """Represents a node in our Knowledge Tree."""
    def __init__(self, title, depth=0):
        self.title = title
        self.depth = depth
        self.children = []

class WikiTopicTree:
    def __init__(self, user_agent="WikiGraphBot/1.0", lang='en'):
        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=lang)
        self.root = None
        
        # AI Filter Setup
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            self.parser = CommaSeparatedListOutputParser()
            self.prompt = ChatPromptTemplate.from_template(
                "You are helping to build a hierarchical taxonomy. Target topic: '{topic}'. "
                "From these related entries: {links}. "
                "Pick the {top_n} most specific sub-fields or directly related children topics that would branch out from '{topic}'. "
                "Return only the titles as a comma-separated list."
            )
            self.chain = self.prompt | self.llm | self.parser
        else:
            self.llm = None

    def get_children_topics(self, topic, links, top_n=3):
        if not self.llm:
            return list(links.keys())[:top_n]
        
        link_titles = list(links.keys())[:15]
        try:
            return self.chain.invoke({"topic": topic, "links": ", ".join(link_titles), "top_n": top_n})
        except:
            return list(links.keys())[:top_n]

    def build_tree(self, root_topic, max_depth=2, branch_factor=3):
        print(f"🌲 Building Knowledge Tree for: {root_topic}")
        self.root = TopicNode(root_topic, depth=0)
        queue = deque([self.root])
        visited = {root_topic}

        while queue:
            current_node = queue.popleft()
            
            if current_node.depth >= max_depth:
                continue
            
            page = self.wiki.page(current_node.title)
            if not page.exists():
                continue

            print(f"🌿 Branching from: {current_node.title} (Level {current_node.depth})")
            
            child_titles = self.get_children_topics(current_node.title, page.links, top_n=branch_factor)
            
            for title in child_titles:
                title = title.strip()
                # In a strict tree, we avoid duplicate nodes in the same hierarchy
                if title not in visited:
                    visited.add(title)
                    child_node = TopicNode(title, depth=current_node.depth + 1)
                    current_node.children.append(child_node)
                    queue.append(child_node)

    def to_networkx(self):
        """Converts our custom tree structure to a NetworkX graph for plotting."""
        G = nx.DiGraph()
        if not self.root:
            return G
        
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            G.add_node(node.title, depth=node.depth)
            for child in node.children:
                G.add_edge(node.title, child.title)
                queue.append(child)
        return G

    def visualize(self):
        G = self.to_networkx()
        if not G.nodes:
            print("Tree is empty!")
            return

        plt.figure(figsize=(14, 10))
        
        # Manual Tree Layout (Recursive)
        pos = self._hierarchy_pos(G, self.root.title)
        
        # Style
        labels = {node: node for node in G.nodes}
        depths = [G.nodes[node]['depth'] for node in G.nodes]
        
        color_map = ["#2d5a27" if d == 0 else ("#4a9c42" if d == 1 else "#a2d49c") for d in depths]
        size_map = [5000 if d == 0 else (3000 if d == 1 else 1500) for d in depths]

        nx.draw(G, pos, labels=labels, with_labels=True, 
                node_color=color_map, node_size=size_map, 
                font_size=9, font_weight="bold", 
                edge_color="#bcbcbc", arrows=True, arrowsize=20)

        plt.title(f"Knowledge Tree: {self.root.title}", fontsize=18, pad=20)
        plt.axis('off')
        
        out_path = "projects/binary_tree/wiki_tree.png"
        plt.savefig(out_path, dpi=300, bbox_inches='tight')
        print(f"📊 Tree visualization saved to {out_path}")

    def _hierarchy_pos(self, G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """
        Custom tree position generator.
        """
        pos = {root: (xcenter, vert_loc)}
        children = list(G.neighbors(root))
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos.update(self._hierarchy_pos(G, child, width=dx, vert_gap=vert_gap, 
                                              vert_loc=vert_loc-vert_gap, xcenter=nextx))
        return pos

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", type=str)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--branch", type=int, default=3)
    args = parser.parse_args()

    tree_maker = WikiTopicTree()
    tree_maker.build_tree(args.topic, max_depth=args.depth, branch_factor=args.branch)
    tree_maker.visualize()
