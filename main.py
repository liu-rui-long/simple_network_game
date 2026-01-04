from src.network import create_network
from src.simulation import Simulation
from src.visualize import plot_cooperation


def main():
    G=create_network()
    sim= Simulation(G)
    ratios=[]
    for i in range(1,100):
        sim.step()
        ratios.append(sim.cooperation_ratio())

    plot_cooperation(ratios)


if __name__ == '__main__':
    main()