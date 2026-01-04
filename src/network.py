import networkx as nx


def create_network(n=100, network_type='BA'):
    if network_type == "ER":   # ER随机图
        return nx.erdos_renyi_graph(n, p=0.05)
    elif network_type == "WS":  # 小世界网络
        return nx.watts_strogatz_graph(n, k=4, p=0.1)
    elif network_type == "BA":  # 无标度网络
        return nx.barabasi_albert_graph(n, m=3)
    else:
        raise ValueError("Unknown network type")