from serpapi import GoogleSearch
import networkx as nx
from tqdm import tqdm
import time
import json
import os
from dotenv import load_dotenv

# === CONFIG ===
load_dotenv()  # Load environment variables from .env file
SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # 🔐 Your API key (hidden in .env)
ROOT_AUTHOR_ID = "6_ecKdsAAAAJ"  # EJ's Google Scholar ID
DEPTH = 1  # 1 = coauthors only; 2 = coauthors of coauthors
SLEEP_TIME = 2  # To avoid getting rate-limited
SAVE_EVERY = 3  # Save progress after every N authors
SAVE_PATH = "../data/scholar_network.json"

# === Initialize the graph ===
G = nx.Graph()

# === Load previous progress if it exists ===
if os.path.exists(SAVE_PATH):
    print("🔄 Loading previous progress...")
    with open(SAVE_PATH, "r") as f:
        data = json.load(f)
        G = nx.node_link_graph(data)
    print(f"✅ Loaded {len(G.nodes())} nodes and {len(G.edges())} edges.")

def fetch_author_data(author_id):
    """Fetch author data from SerpApi"""
    search = GoogleSearch({
        "engine": "google_scholar_author",
        "author_id": author_id,
        "api_key": SERPAPI_KEY
    })
    result = search.get_dict()
    return result

def add_author_to_graph(author_data):
    """Add author, papers, and coauthors to the graph"""
    author_name = author_data.get("author", {}).get("name", "Unknown")
    G.add_node(author_name, type="Author")

    # Add paper nodes
    for art in author_data.get("articles", []):
        paper_title = art.get("title")
        if not paper_title:
            continue
        G.add_node(paper_title, type="Paper")
        G.add_edge(author_name, paper_title, relation="authored")

    # Add coauthor nodes
    for co in author_data.get("co_authors", []):
        co_name = co.get("name")
        co_id = co.get("author_id")
        if co_name:
            G.add_node(co_name, type="Author")
            G.add_edge(author_name, co_name, relation="coauthor", co_id=co_id)

def save_progress():
    """Save the current progress to a JSON file"""
    with open(SAVE_PATH, "w") as f:
        json.dump(nx.node_link_data(G), f, indent=2)
    print(f"💾 Progress saved ({len(G.nodes())} nodes, {len(G.edges())} edges).")

def crawl_graph(root_id, depth=1):
    """Recursively crawl the coauthor network (with checkpoint saving)"""
    visited = set(nx.get_node_attributes(G, "type").keys())  # Already existing nodes
    queue = [(root_id, 0)]

    counter = 0
    while queue:
        author_id, level = queue.pop(0)
        if author_id in visited:
            continue
        visited.add(author_id)

        try:
            data = fetch_author_data(author_id)
        except Exception as e:
            print(f"⚠️ Error fetching {author_id}: {e}")
            break

        try:
            add_author_to_graph(data)
        except Exception as e:
            print(f"⚠️ Error adding author to graph: {e}")
            continue

        counter += 1
        if counter % SAVE_EVERY == 0:
            save_progress()

        # Control the crawling depth
        if level < depth:
            for co in data.get("co_authors", []):
                co_id = co.get("author_id")
                if co_id:
                    queue.append((co_id, level + 1))

        time.sleep(SLEEP_TIME)

    save_progress()

# === Run the crawler ===
print(f"Fetching network from author ID: {ROOT_AUTHOR_ID}")
crawl_graph(ROOT_AUTHOR_ID, depth=DEPTH)
print(f"✅ Finished: {len(G.nodes())} nodes, {len(G.edges())} edges saved to {SAVE_PATH}")
