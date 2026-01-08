class AgenteBase:
    def __init__(self, nome, modo="test", start=(0,0)):
        self.nome = nome
        self.modo = modo
        self.start = start
        self.current_obs = None
        self.sensores = []

    def observacao(self, obs):
        self.current_obs = obs

    def age(self):
        raise NotImplementedError

    def avaliacaoEstadoAtual(self, recompensa):
        pass

    def reset(self):
        self.current_obs = None

    def instala(self, sensor):
        self.sensores.append(sensor)
    
    def processar_sensores(self, ambiente):
        # O agente constrói a sua percepção através dos sensores instalados
        percepcao = {}
        for s in self.sensores:
            percepcao.update(s.ler(ambiente, self))
        self.current_obs = percepcao