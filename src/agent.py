
import numpy as np
import random


class Agent():
    def __init__(self, strategy, alpha=None, gamma=0.9, epsilon_decay=None):
        self.strategy = strategy
        self.payoff = 0.0

        self.alpha = alpha if alpha is not None else random.uniform(0.01, 0.1)  # 学习率
        self.gamma = gamma  # 折扣率
        self.epsilon = 1.0  # 探索率
        self.epsilon_min = 0.05  # 最小的探索率
        self.epsilon_decay = epsilon_decay if epsilon_decay is not None else random.uniform(0.8, 0.995)  # 探索衰减率

        self.q_table = np.zeros((4, 2))  # 初始化Q表 2状态(0背叛/1合作)两动作
        # 记录当前状态和动作，用于Q更新
        self.prev_state = None
        self.prev_action = None
        self.last_delta_Q = 0.0  # 记录q值的变化

    def choose_action(self, state):

        if random.random() < self.epsilon:
            action = random.choice([0, 1])
        else:
            action = np.argmax(self.q_table[state])
        self.prev_state = state
        self.prev_action = action

        # ε 衰减
        self.epsilon = max(self.epsilon_min,
                           self.epsilon * self.epsilon_decay)
        return action

    def update_q(self, next_state):

        prev_Q = self.q_table.copy()  # 复制一份q表，用于计算
        reward = self.payoff
        next_Q = np.max(self.q_table[next_state])

        td_target = reward + self.gamma * next_Q
        td_error = td_target - self.q_table[self.prev_state, self.prev_action]
        self.q_table[self.prev_state, self.prev_action] += self.alpha * td_error

        self.last_delta_Q = np.max(np.abs(self.q_table - prev_Q))  # 记录q表变化最大值
