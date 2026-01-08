import json
from src.ambiente.grid import GridEnvironment
from src.ambiente.maze import MazeEnvironment
from src.agentes.agente_fixo import FixedAgent
from src.agentes.learning_agente import QLearningAgent
from src.logger.logger import Logger

class Simulador:
    def __init__(self, params_file: str):
        with open(params_file, 'r') as f:
            self.params = json.load(f)

        self.agentes = []
        self.ambiente = None
        self.logger = Logger()
        self._build_from_params()

    def listaAgentes(self):
        return self.agentes

    def _build_from_params(self):
        p = self.params
        
        if p.get("problem") == "maze":
            self.ambiente = MazeEnvironment(
                p["width"], p["height"], tuple(p["target"]), p["walls"], p.get("max_steps_per_episode", 100)
            )
        else:
            self.ambiente = GridEnvironment(
                p["width"], p["height"], tuple(p["target"]), p.get("max_steps_per_episode", 100)
            )

        for a in p.get("agents", []):
            modo = a.get("modo", "learn") # "learn" ou "test"
            
            if a["type"] == "fixed":
                ag = FixedAgent(a["name"], start=tuple(a["start"]), modo="test")
            elif a["type"] == "qlearn":
                ag = QLearningAgent(
                    a["name"], alpha=a.get("alpha", 0.1), gamma=a.get("gamma", 0.9),
                    epsilon=a.get("epsilon", 0.1), start=tuple(a["start"]), modo=modo
                )
                # Se houver um ficheiro de política e estivermos em modo teste, carrega
                if modo == "test" and "policy_file" in a:
                    ag.carregar_politica(a["policy_file"])
            
            self.agentes.append(ag)
            self.ambiente.add_agent(ag)

    def executa(self, n_episodes=None):
        if n_episodes is None:
            n_episodes = self.params.get("n_episodes", 1)

        for ep in range(n_episodes):
            self.ambiente.reset()
            for ag in self.agentes: ag.reset()

            done = False
            steps = 0
            rewards = {ag.nome: 0 for ag in self.agentes}

            while not done and steps < self.params["max_steps_per_episode"]:
                # PERCEPÇÃO: Apenas um bloco para observação
                for ag in self.agentes:
                    if hasattr(ag, 'sensores') and ag.sensores:
                        percepcao = {}
                        for s in ag.sensores:
                            percepcao.update(s.ler(self.ambiente, ag))
                        ag.observacao(percepcao)
                    else:
                        ag.observacao(self.ambiente.observacaoPara(ag))

                # DELIBERAÇÃO
                actions = {ag: ag.age() for ag in self.agentes}

                # EXECUÇÃO E RECOMPENSA
                for ag, ac in actions.items():
                    r = self.ambiente.agir(ac, ag)
                    rewards[ag.nome] += r
                    ag.avaliacaoEstadoAtual(r) # Aqui ocorre o Q-Learning se modo="learn"

                done = self.ambiente.atualizacao()
                steps += 1

            for name, r in rewards.items():
                self.logger.registar(ep, name, r, steps)

        self.logger.guardar("results/results.csv")