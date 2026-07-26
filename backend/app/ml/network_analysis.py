"""
Crime network analysis over the `relationships` edge table.
Builds a NetworkX graph on demand and computes centrality, communities,
and shortest paths — powers the Cytoscape.js graph in the frontend.
"""
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


def build_graph(edges: list[dict]) -> nx.Graph:
    g = nx.Graph()
    for e in edges:
        src = f"{e['source_type']}:{e['source_id']}"
        tgt = f"{e['target_type']}:{e['target_id']}"
        g.add_node(src, type=e["source_type"])
        g.add_node(tgt, type=e["target_type"])
        g.add_edge(src, tgt, relationship=e["relationship_type"], weight=e.get("weight", 1.0))
    return g


def analyze(edges: list[dict]) -> dict:
    g = build_graph(edges)
    if g.number_of_nodes() == 0:
        return {"nodes": [], "edges": [], "communities": [], "centrality": {}}

    centrality = nx.betweenness_centrality(g, weight="weight")
    pagerank = nx.pagerank(g, weight="weight")
    communities = [list(c) for c in greedy_modularity_communities(g, weight="weight")]

    nodes = [
        {
            "id": n,
            "type": g.nodes[n].get("type"),
            "betweenness": round(centrality.get(n, 0), 4),
            "pagerank": round(pagerank.get(n, 0), 4),
            "degree": g.degree(n),
        }
        for n in g.nodes
    ]
    edge_list = [
        {"source": u, "target": v, "relationship": d.get("relationship"), "weight": d.get("weight")}
        for u, v, d in g.edges(data=True)
    ]
    return {
        "nodes": nodes,
        "edges": edge_list,
        "communities": [{"id": i, "members": members} for i, members in enumerate(communities)],
    }


def shortest_path(edges: list[dict], source: str, target: str) -> list[str] | None:
    g = build_graph(edges)
    try:
        return nx.shortest_path(g, source=source, target=target, weight="weight")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None
