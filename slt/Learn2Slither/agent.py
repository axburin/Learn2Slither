import ast
import json
import os
import random


ACTIONS = [0, 1, 2, 3]


class Agent:
    def __init__(self, alpha=0.1, gamma=0.9,
                 epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995,
                 learning=True):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning = learning
        self.q_table = {}  # {state_tuple: [q0, q1, q2, q3]}

    # ── Q-table helpers ───────────────────────────────────────────────────────

    def _get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]
        return self.q_table[state]

    # ── Action selection ──────────────────────────────────────────────────────

    def get_action(self, state):
        """Epsilon-greedy action selection."""
        if self.learning and random.random() < self.epsilon:
            return random.choice(ACTIONS)
        q = self._get_q(state)
        max_q = max(q)
        best = [i for i, v in enumerate(q) if v == max_q]
        return random.choice(best)

    # ── Q-learning update ─────────────────────────────────────────────────────

    def update(self, state, action, reward, next_state, done):
        if not self.learning:
            return
        q = self._get_q(state)
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self._get_q(next_state))
        q[action] = q[action] + self.alpha * (target - q[action])

    def decay_epsilon(self):
        if self.learning:
            self.epsilon = max(
                self.epsilon * self.epsilon_decay, self.epsilon_min
            )

    # ── Persistence ───────────────────────────────────────────────────────────

    def save(self, path):
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        data = {
            'alpha': self.alpha,
            'gamma': self.gamma,
            'epsilon': self.epsilon,
            'epsilon_min': self.epsilon_min,
            'epsilon_decay': self.epsilon_decay,
            'q_table': {str(k): v for k, v in self.q_table.items()},
        }
        with open(path, 'w') as f:
            json.dump(data, f)

    def load(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        self.alpha = data.get('alpha', self.alpha)
        self.gamma = data.get('gamma', self.gamma)
        self.epsilon = data.get('epsilon', self.epsilon_min)
        self.epsilon_min = data.get('epsilon_min', self.epsilon_min)
        self.epsilon_decay = data.get('epsilon_decay', self.epsilon_decay)
        self.q_table = {
            ast.literal_eval(k): v
            for k, v in data['q_table'].items()
        }
