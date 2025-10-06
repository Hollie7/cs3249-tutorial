# ============================================================
# visualize_graph.py
# ============================================================

import json
import networkx as nx
from pyvis.network import Network
import os

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(__file__)  
GRAPH_PATH = os.path.join(BASE_DIR, "graph_sample_data.json")
OUTPUT_HTML = "graph_visualization.html"

# ---------- LOAD GRAPH ----------
print(f"📂 Loading graph from {GRAPH_PATH} ...")
with open(GRAPH_PATH, "r") as f:
    graph_data = json.load(f)

# Use node_link_graph and enforce a directed graph (for compatibility with future versions)
G = nx.node_link_graph(graph_data, edges="links", directed=True)
if not isinstance(G, nx.DiGraph):
    G = nx.DiGraph(G)

print(f"✅ Graph loaded: {len(G.nodes())} nodes, {len(G.edges())} edges")

# ---------- CREATE PyVis NETWORK ----------
net = Network(height="800px", width="100%", directed=True, notebook=False)
net.barnes_hut()  # Use automatic force-directed layout

# Color nodes by type
color_map = {
    "Author": "#FF7F50",  # Coral orange
    "Paper": "#87CEEB",   # Sky blue
    "Unknown": "#D3D3D3"  # Light gray
}

for node, data in G.nodes(data=True):
    n_type = data.get("type", "Unknown")
    color = color_map.get(n_type, "#D3D3D3")
    title = f"{n_type}: {node}"
    net.add_node(node, label=node, color=color, title=title)

# Add edges with relation labels
for source, target, data in G.edges(data=True):
    relation = data.get("relation", "")
    net.add_edge(source, target, label=relation)

# ---------- EXPORT TO HTML ----------
net.set_options("""
var options = {
  "edges": {
    "color": {"inherit": true},
    "smooth": false
  },
  "physics": {
    "enabled": true,
    "barnesHut": {
      "gravitationalConstant": -5000,
      "springLength": 150
    }
  },
  "interaction": {
    "hover": true,
    "multiselect": true,
    "navigationButtons": true
  }
}
""")

net.write_html(OUTPUT_HTML)
print(f"🌐 Visualization saved to {OUTPUT_HTML}")
print("👉 Open this file in your browser manually to explore the graph.")
