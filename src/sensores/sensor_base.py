class Sensor:
    """
    Classe base para sensores. Um sensor pode ler
    alguma informação do ambiente e passar ao agente.
    """

    def ler(self, ambiente, agente):
        """
        Deve devolver uma parte da observação do ambiente.
        Cada sensor terá a sua implementação própria.
        """
        raise NotImplementedError("O sensor deve implementar o método ler().")