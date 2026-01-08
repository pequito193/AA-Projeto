from src.ambiente.base import AmbienteBase

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "STAY"]

class GridEnvironment(AmbienteBase):
    def __init__(self, width, height, target, max_steps=100):
        self.width = width
        self.height = height
        self.target = tuple(target)
        self.max_steps = max_steps

        self.agents = {}
        self.positions = {}
        self.step_count = 0

    def add_agent(self, agent):
        self.agents[agent.nome] = agent
        self.positions[agent.nome] = agent.start

    def reset(self):
        self.step_count = 0
        for ag in self.agents.values():
            self.positions[ag.nome] = ag.start

    def observacaoPara(self, agente):
        return {
            "self_pos": self.positions[agente.nome],
            "target": self.target,
            "grid_size": (self.width, self.height)
        }

    def agir(self, acao, agente):
        x, y = self.positions[agente.nome]

        if acao == "UP":
            y = max(0, y - 1)
        elif acao == "DOWN":
            y = min(self.height - 1, y + 1)
        elif acao == "LEFT":
            x = max(0, x - 1)
        elif acao == "RIGHT":
            x = min(self.width - 1, x + 1)

        self.positions[agente.nome] = (x, y)

        if (x, y) == self.target:
            return 1.0
        return -0.01

    def atualizacao(self):
        self.step_count += 1

        all_reached = all(pos == self.target for pos in self.positions.values())
        if all_reached:
            return True

        if self.step_count >= self.max_steps:
            return True

        return False
