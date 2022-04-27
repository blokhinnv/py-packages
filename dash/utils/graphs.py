import networkx as nx

def karate_graph(scale=200):
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, seed=42)
    # elements - это список словарей
    # каждый элемент имеет ключ data - характеристики узла в виде словаря
    # у узлов - доп ключ position
    # у ребер - в data есть ключи source и target
    elements = []
    for node, data in G.nodes(data=True):
        # у каждого узла должен быть ID
        data["id"] = node
        # если у узла есть label, он будет подписан
        data["label"] = f"Узел {node}"
        x, y = pos[node] * scale
        position = {"x": x, "y": y}
        elements.append({
            "data": data,
            "position": position
        })
    for u, v in G.edges:
        elements.append({
            "data": {"source": u, "target": v}
        })
    return elements
