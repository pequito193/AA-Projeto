class AmbienteBase:
    def observacaoPara(self, agente):
        raise NotImplementedError

    def agir(self, acao, agente):
        raise NotImplementedError

    def atualizacao(self):
        raise NotImplementedError
