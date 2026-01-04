import numpy as np
import random


def fermi_update(agent_i,agent_j,beta=1.0):
    prob=1/(1+np.exp(-beta*(agent_i.payoff-agent_j.payoff)))
    if random.random()<prob:
        agent_i.payoff=agent_j.payoff