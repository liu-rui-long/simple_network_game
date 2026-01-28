import math
import networkx as nx
SEED = 42


def create_network(n=100, network_type='BA'):
    if network_type == "ER":  # ER随机图
        return nx.erdos_renyi_graph(n, p=0.05, seed=SEED)  # p为任意俩存在边的概率
    elif network_type == "WS":  # 小世界网络
        return nx.watts_strogatz_graph(n, k=4, p=0.1, seed=SEED)  # k初始邻居p重连率
    elif network_type == "BA":  # 无标度网络
        return nx.barabasi_albert_graph(n, m=3, seed=SEED)  # m新节点连接个数
    elif network_type == "Star":  # 星型网络
        return nx.star_graph(n - 1)
    elif network_type == "Grid_1":  # 冯诺依曼领域为1的格子网络
        return create_grid_network(n, radius=1)
    elif network_type == "Grid_2":  # 冯诺依曼领域为2的格子网络
        return create_grid_network(n, radius=2)
    else:
        raise ValueError("Unknown network type")


def create_grid_network(n, radius=1):
    size = int(math.sqrt(n))
    if size*size != n:
        n = size*size
        print('n数值有问题')
    # 创建一个一维图,添加所有的节点
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    # 为每个节点添加邻居
    for node in range(n):
        # 一维转二维，行优先
        i = node//size
        j = node % size

        # 遍历所有方向的邻居
        for di in range(-radius, radius+1):
            for dj in range(-radius, radius+1):
                if di == 0 and dj == 0:  # 跳过自己
                    continue
                # 曼哈顿距离检查
                if abs(di)+abs(dj) <= radius:
                    # 周期性边界
                    ni = (i+di) % size
                    nj = (j+dj) % size
                    neighbors = ni*size+nj

                    if node < neighbors:  # 这个地方是优化，不加也可以，会自己去重边
                        G.add_edge(node, neighbors)

    return G
