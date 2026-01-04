from src.agent import Agent
from src.game import play_game
from src.dynamics import fermi_update
import random


class Simulation(object):
    def __init__(self,graph):
        self.graph=graph
        self.agents={i:Agent(random.choice([0,1])) for i in graph.nodes()}

    def step(self):
        for agent in self.agents.values():
            agent.payoff = 0

        for i,j in self.graph.edges():
            p_i,p_j=play_game(self.agents[i].strategy,self.agents[j].strategy)
            self.agents[i].payoff += p_i
            self.agents[j].payoff += p_j
        for i in self.graph.nodes():
            neighbor=random.choice(list(self.graph.neighbors(i)))
            fermi_update(self.agents[i],self.agents[j])

    def cooperation_ratio(self):

        return sum(a.strategy for a in self.agents.values())/len(self.agents)
