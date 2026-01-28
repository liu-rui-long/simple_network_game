import matplotlib.pyplot as plt
import networkx as nx


def plot_cooperation(ratios, graph, gname):

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].set_title('network')
    nx.draw(graph, ax=axes[0], with_labels=True)

    axes[1].set_title(f'Cooperation------{gname}')
    axes[1].set_xlabel('Time Step')
    axes[1].set_ylabel('Cooperation Ratio')
    axes[1].plot(ratios)

    plt.tight_layout()
    plt.show()


def plot_network_strategy(graph, agents, step=0):
    """
    可视化网络结构，节点颜色表示策略
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph, seed=66)  # 使用spring_layout算法来计算每个节点在图形中的位置。seed种子保持布局一致


    # 按策略分类节点
    cooperators = [node for node, agent in agents.items() if agent.strategy == 1]
    defectors = [node for node, agent in agents.items() if agent.strategy == 0]

    # 绘制边
    nx.draw_networkx_edges(graph, pos, alpha=0.3)

    # 绘制合作者节点
    nx.draw_networkx_nodes(graph, pos, nodelist=cooperators,
                           node_color='blue', node_size=100, label='Cooperator')

    # 绘制背叛者节点
    nx.draw_networkx_nodes(graph, pos, nodelist=defectors,
                           node_color='red', node_size=100, label='Defector')

    plt.title(f"Strategy Distribution (Step {step})")
    plt.legend()
    plt.axis('off')
    plt.show()

def plot_delta_q(mean_delta_q):
    plt.plot(mean_delta_q)
    plt.xlabel("Time")
    plt.ylabel("Average ΔQ")
    plt.title("Q-learning Convergence")
    plt.show()
