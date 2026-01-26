from src.network import create_network
from src.simulation import Simulator
from src.visualize import plot_cooperation,plot_delta_q
import numpy as np
import random

SEED = 42
np.random.seed(SEED)
random.seed(SEED)


def main():
    # G=['BA','WS','ER']
    G=['Grid_1']
    for g in G:
        graph=create_network(100, g)
        sim = Simulator(graph, 'IB', 'dynamic')
        # agents=sim.agents
        ratios = []
        for i in range(1500):
            sim.step2()
            ratios.append(sim.cooperation_ratio())
        plot_cooperation(ratios, graph, g)
        plot_delta_q(sim.delta_q())
        # plot_network_strategy(graph, agents, step=0)


if __name__ == '__main__':
    main()