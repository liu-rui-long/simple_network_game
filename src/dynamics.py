import numpy as np
import random


def fermi_update(agent_i, agent_j, beta=1.0):
    prob = 1/(1+np.exp(-beta*(agent_i.payoff-agent_j.payoff)))
    if random.random() < prob:
        agent_i.payoff = agent_j.payoff


def imitate_best(agent_i, neighbors):
    if neighbors:
        best = max(neighbors, key=lambda x: x.payoff)
        if best.payoff > agent_i.payoff:  # 这里也可以设置一个参数，当明显高于的时候才模仿
            agent_i.strategy = best.strategy
