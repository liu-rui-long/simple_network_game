from src.agent import Agent
from src.game import play_game
from src.dynamics import fermi_update, imitate_best
import networkx as nx
import numpy as np
import random


class Simulator():

    def __init__(self, graph, dynamic_type, network_dynamic='static', rewire_prob=0.01, homophily=0.7):
        self.graph = graph
        self.dynamic_type = dynamic_type  # 策略更新方式
        self.network_dynamic = network_dynamic  # 是否动态网络
        self.rewire_prob = rewire_prob  # 断边率
        self.agents = {i: Agent(random.choice([0, 1])) for i in graph.nodes()}
        self.homophily = homophily  # 同质性因子
        self.avg_delta_q = []  # 记录每一步所有个体平均最大q差的变化

    def neighbor_coop_ratio(self,agent_id):
        neighbors = list(self.graph.neighbors(agent_id))
        if len(neighbors) == 0:
            return 0
        coop_ratio = sum(self.agents[i].strategy for i in neighbors)
        if coop_ratio/len(neighbors) > 0.5:
            return 1
        else:
            return 0

    def update_network1(self):  # 随机重连，以rewire_prob断开
        all_edges = list(self.graph.edges())
        for u, v in all_edges:  # 收集需要重连的边
            if random.random() < self.rewire_prob:
                self.graph.remove_edge(u, v)  # 移除边
                if nx.is_connected(self.graph):  # 保证网络连通，不连通则回滚
                    possible_node = [n for n in self.graph.nodes if n != u and n not in self.graph.neighbors(u)]
                    if possible_node:  # 找重连的节点，不能是u本身和u已有的连接
                        new_v = random.choice(possible_node)
                        self.graph.add_edge(u, new_v)
                    else:
                        self.graph.add_edge(u, v)
                else:
                    self.graph.add_edge(u, v)

    def update_network2(self):  # 考虑策略的同质性,对于同策略有homophily概率保持，不同则1-h保持
        all_edges = list(self.graph.edges())
        for u, v in all_edges:
            agent_u = self.agents[u]
            agent_v = self.agents[v]
            if agent_u.strategy == agent_v.strategy:
                keep_prob = self.homophily
            else:
                keep_prob = 1 - self.homophily
            if random.random() > keep_prob:
                self.graph.remove_edge(u, v)

                if nx.is_connected(self.graph):
                    same_strategy = [x for x in self.graph.nodes
                                     if (x != u and self.agents[x].strategy == agent_u.strategy
                                         and x not in self.graph.neighbors(u))
                                     ]
                    if same_strategy:
                        self.graph.add_edge(u, random.choice(same_strategy))
                    else:
                        self.graph.add_edge(u, v)
                else:
                    self.graph.add_edge(u, v)

    '''  Q-learning 负责价值评估与决策，Fermi 负责随机性、扩散与结构演化
       两者可在行为、学习和网络三个层次以不同方式耦合
       目前常见的Q-learning和费米等结合
       1.Q-learning用于个体的学习，费米用于个体对群体的学习，最后决定是用自己的学习还是群体的学习
       2.Q-learning用于评估行为得到Q值，Q值被用于费米决定是否模仿
       3.Q-learning用于行为决策，费米用于更新网络
       4.Q-learning决定学什么，费米决定学不学
       '''
    def step1(self):
        for agent in self.agents.values():
            agent.payoff = 0.0
        for i, j in self.graph.edges():  # 计算收益
            p_i, p_j=play_game(self.agents[i].strategy, self.agents[j].strategy, 'SH')
            self.agents[i].payoff += p_i
            self.agents[j].payoff += p_j
        for i in self.graph.nodes():  # 策略更新
            neighbors = [self.agents[x] for x in self.graph.neighbors(i)]
            if self.dynamic_type == 'FM':
                neighbor = random.choice(list(self.graph.neighbors(i)))
                fermi_update(self.agents[i], self.agents[neighbor])
            elif self.dynamic_type == 'IB':
                imitate_best(self.agents[i], neighbors)
        if self.network_dynamic == 'dynamic':
            self.update_network2()

    def step2(self):
        actions = {}
        for i, agent in self.agents.items():  # 选动作，清空收益，合作率是上一轮的
            pre_ratio = self.neighbor_coop_ratio(i)
            state = agent.strategy * 2 + pre_ratio
            action = agent.choose_action(state)
            actions[i] = action
            agent.payoff = 0
        for i, action in actions.items():  # 这里采用同步更新
            self.agents[i].strategy = action

        for i, j in self.graph.edges():  # 计算收益
            p_i, p_j = play_game(self.agents[i].strategy,
                                 self.agents[j].strategy,
                                 'SH')
            self.agents[i].payoff += p_i
            self.agents[j].payoff += p_j

        for i, agent in self.agents.items():  # 更新Q表
            ratio = self.neighbor_coop_ratio(i)
            next_state = agent.strategy * 2 + ratio
            agent.update_q(next_state)

        mean_delta_q = np.mean([agent.last_delta_Q for agent in self.agents.values()])
        self.avg_delta_q.append(mean_delta_q)  # 记录所以个体的平均q差

    def cooperation_ratio(self):  # 合作者占的比例,还可以加平均度、聚类系数等
        return sum(a.strategy for a in self.agents.values())/len(self.agents)

    def delta_q(self):
        return self.avg_delta_q

