import random
import json
from src.agentes.base import AgenteBase

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

def state_from_obs(obs):
    # Converte o dicionário de observação num tuplo (imutável) para ser chave no dicionário Q
    sx, sy = obs["self_pos"]
    tx, ty = obs["target"]
    return (sx, sy, tx, ty)

class QLearningAgent(AgenteBase):
    def __init__(self, nome, alpha=0.1, gamma=0.9, epsilon=0.1, start=(0,0), modo="learn"):
        super().__init__(nome, modo, start)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.Q = {}
        self.last_state = None
        self.last_action = None

    def _get_Q(self, s):
        if str(s) not in self.Q:
            self.Q[str(s)] = {a: 0.0 for a in ACTIONS}
        return self.Q[str(s)]

    def escolher_acao(self, s):
        # No modo de teste, a exploração (epsilon) é ignorada
        if self.modo == "learn" and random.random() < self.epsilon:
            return random.choice(ACTIONS)
        
        q = self._get_Q(s)
        maxv = max(q.values())
        best = [a for a, v in q.items() if v == maxv]
        return random.choice(best)

    def age(self):
        s = state_from_obs(self.current_obs)
        a = self.escolher_acao(s)
        self.last_state = s
        self.last_action = a
        return a

    def atualizar_epsilon(self, decay=0.999, min_epsilon=0.01):
        if self.modo == "learn":
            self.epsilon = max(min_epsilon, self.epsilon * decay)

    def avaliacaoEstadoAtual(self, r):
        # No modo de teste, não há atualização da tabela Q
        if self.modo == "test" or self.last_state is None:
            return

        s = state_from_obs(self.current_obs)
        q_prev = self._get_Q(self.last_state)
        q_next = self._get_Q(s)
        a = self.last_action

        # Fórmula do Q-Learning
        # Q(S, A) = Q(S, A) + alpha * (R + gamma * max(Q(S', a')) - Q(S, A))
        q_prev[a] += self.alpha * (r + self.gamma * max(q_next.values()) - q_prev[a])

    # Métodos de Persistência para o Modo de Teste
    def guardar_politica(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.Q, f)
        print(f"Política do agente {self.nome} guardada em {filename}")

    def carregar_politica(self, filename):
        with open(filename, 'r') as f:
            self.Q = json.load(f)
        print(f"Política do agente {self.nome} carregada de {filename}")