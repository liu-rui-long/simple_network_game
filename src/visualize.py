import matplotlib.pyplot as plt

def plot_cooperation(ratios):
    plt.plot(ratios)
    plt.xlabel("Time Step")
    plt.ylabel("Cooperation Ratio")
    plt.show()