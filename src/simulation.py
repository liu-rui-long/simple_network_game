from src.agent import Agent
from src.game import play_game
from src.dynamics import fermi_update,imitate_best
import networkx as nx
import random


class Simulator():

    def __init__(self,graph,dynamic_type,network_dynamic,rewire_prob=0.01,homophily=0.7):
        self.graph = graph
        self.dynamic_type = dynamic_type
        self.network_dynamic = network_dynamic
        self.rewire_prob = rewire_prob
        self.agents ={i:Agent(random.choice([0,1])) for i in graph.nodes()}
        self.homophily=homophily # 同质性因子

    def update_network1(self):  # 随机重连，以rewire_prob断开
        rewire_edges=[]
        for u,v in self.graph.edges():  # 收集需要重连的边,考虑两个节点的度都是大于1，保证网络连通
            if random.random() < self.rewire_prob and nx.is_connected(self.graph):
                rewire_edges.append((u,v))
        for u,v in rewire_edges:  # 移除边，找重连的节点，不能是u本身和u已有的连接
            self.graph.remove_edge(u,v)
            possible_node = [n for n in self.graph.nodes if n != u and n not in self.graph.neighbors(u)]
            if possible_node:
                new_v = random.choice(possible_node)
                self.graph.add_edge(u,new_v)
            else:
                self.graph.add_edge(u,v)

    def update_network2(self):  #考虑策略的同质性,对于同策略有homophily概率保持，不同则1-h保持
        all_egdes = list(self.graph.edges())
        for u,v in all_egdes:
            agent_u = self.agents[u]
            agent_v = self.agents[v]
            if agent_u.strategy == agent_v.strategy:
                keep_prob = self.homophily
            else:
                keep_prob = 1-self.homophily
            if random.random() > keep_prob :
                self.graph.remove_edge(u,v)

                if nx.is_connected(self.graph):
                    same_strategy=[x for x in self.graph.nodes
                                   if (x != u and self.agents[x].strategy == agent_u.strategy and x not in self.graph.neighbors(u))
                                  ]
                    if same_strategy:
                        self.graph.add_edge(u,random.choice(same_strategy))
                    else:
                        self.graph.add_edge(u,v)
                else:
                    self.graph.add_edge(u, v)






    def step(self):
        for agent in self.agents.values():
            agent.payoff = 0.0
        for i,j in self.graph.edges():  #计算收益
            p_i,p_j=play_game(self.agents[i].strategy,self.agents[j].strategy,'SH')
            self.agents[i].payoff += p_i
            self.agents[j].payoff += p_j
        for i in self.graph.nodes():  #策略更新
            neighbors = [self.agents[x] for x in self.graph.neighbors(i)]
            if self.dynamic_type=='FM':
                neighbor = random.choice(list(self.graph.neighbors(i)))
                fermi_update(self.agents[i],self.agents[neighbor])
            elif self.dynamic_type=='IB':
                imitate_best(self.agents[i], neighbors)
        if self.network_dynamic=='dynamic':
            self.update_network2()


    def cooperation_ratio(self):
        return sum(a.strategy for a in self.agents.values())/len(self.agents)