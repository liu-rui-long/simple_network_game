from src.network import create_network
from src.simulation import Simulation
from src.visualize import plot_cooperation


def main():
    G=['Star','WS']
    for g in G:
        graph=create_network(100,g)
        sim = Simulation(graph)
        # agents=sim.agents
        ratios=[]
        for i in range(10):
            sim.step()
            ratios.append(sim.cooperation_ratio())
        plot_cooperation(ratios, graph,g)
        # plot_network_strategy(graph, agents, step=0)
if __name__ == '__main__':
    main()