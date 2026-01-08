from src.ambiente.grid import GridEnvironment

class MazeEnvironment(GridEnvironment):
    def __init__(self, width, height, target, walls, max_steps=100):
        super().__init__(width, height, target, max_steps)
        # Conjunto de tuplos para busca rápida de paredes
        self.walls = set(tuple(w) for w in walls)

    def agir(self, acao, agente):
        old_x, old_y = self.positions[agente.nome]
        x, y = old_x, old_y

        if acao == "UP": y = max(0, y - 1)
        elif acao == "DOWN": y = min(self.height - 1, y + 1)
        elif acao == "LEFT": x = max(0, x - 1)
        elif acao == "RIGHT": x = min(self.width - 1, x + 1)

        # Lógica de colisão com paredes
        if (x, y) in self.walls:
            return -0.5  # Penalização por colisão
        
        self.positions[agente.nome] = (x, y)

        if (x, y) == self.target:
            return 10000.0  # Recompensa por encontrar a saída
        
        return -0.05  # Custo por passo no labirinto