# %%
import networkx as nx
import matplotlib.pyplot as plt

Network = nx.Graph()

Network.add_node("S1", ip_A1="192.168.0.97", ip_A2="192.168.0.113")
Network.add_node("A1", ip="192.168.0.98")
Network.add_node("A2", ip="192.168.0.114")

Network.add_node("E1", ip=f"192.168.0.2")
Network.add_node("E2", ip=f"192.168.0.34")

Network.add_node("E3", ip=f"192.168.0.66")
Network.add_node("E4", ip="192.168.0.82")


Network.add_edge("S1", "A1", peso=10)

Network.add_edge("A1", "E1", peso=3)
Network.add_edge("A1", "E2", peso=3)

Network.add_edge("S1", "A2", peso=10)

Network.add_edge("A2", "E3", peso=2)
Network.add_edge("A2", "E4", peso=2)

# Hosts da subrede E1 192.168.0.3 a 7
for i in range(3, 8):
    host = f"H{i}"
    Network.add_node(host, ip=f"192.168.0.{i}")
    Network.add_edge("E1", host, peso=5)

# Hosts da subrede E2 192.168.0.35 a 41
for i in range(35, 42):
    host = f"H{i}"
    Network.add_node(host, ip=f"192.168.0.{i}")
    Network.add_edge("E2", host, peso=2)

# Hosts da subrede E3 192.168.0.67 a 74
for i in range(67, 75):
    host = f"H{i}"
    Network.add_node(host, ip=f"192.168.0.{i}")
    Network.add_edge("E3", host, peso=4)

# Hosts da subrede E4 192.168.0.83 a 88
for i in range(83, 89):
    host = f"H{i}"
    Network.add_node(host, ip=f"192.168.0.{i}")
    Network.add_edge("E4", host, peso=4)


def ping(G: nx.Graph, source: str, dest: str, num_tries: int):
    assert G.has_node(source)
    assert G.has_node(dest)

    ip_source = G.nodes[source]["ip"]
    ip_dest = G.nodes[dest]["ip"]
    print(f"PING {source} ({ip_source}) -> {dest} ({ip_dest})")

    caminho = nx.shortest_path(G, source, dest)
    for i in range(1, num_tries + 1):
        soma_tempo = 0
        for index, node in enumerate(caminho):
            if index == len(caminho) - 1:
                break
            soma_tempo += G[node][caminho[index + 1]]["peso"]
        print(f"Recebeu de {ip_dest} icmp_seq={i} rtt={soma_tempo*2} ms")


def traceroute(G: nx.Graph, source: str, dest: str):
    assert G.has_node(source)
    assert G.has_node(dest)
    ip_source = get_ip(G, source)
    ip_dest = get_ip(G, dest)

    print(f"Traceroute from {ip_source} to {ip_dest}")
    caminho = nx.shortest_path(G, source, dest)[1:]
    soma_tempo = 0
    anterior = source
    for i, proximo in enumerate(caminho):
        edge = G[anterior][proximo]
        ip_proximo = (
            get_ip(G, proximo)
            if proximo != "S1"
            else G.nodes[proximo][f"ip_{anterior}"]
        )
        soma_tempo += edge["peso"] * 2
        print(
            f"{i+1}  {proximo}({ip_proximo})",
            f"{soma_tempo} ms",
        )
        anterior = proximo


def get_ip(G: nx.Graph, node: str):
    assert G.has_node(node)
    return G.nodes[node]["ip"]


nx.draw(
    Network,
    node_size=550,
    font_color="white",
    with_labels=True,
    node_color="blue",
    edge_color="darkblue",
)
plt.show()

source = "H4"
dest = "H84"
print(nx.shortest_path(Network, source, dest))
print()
ping(Network, source, dest, 5)
print()
traceroute(Network, source, dest)
