from src.sensores.sensor_base import Sensor

class ProximitySensorImplementacaoInicial(Sensor):
    def ler(self, ambiente, agente):
        x, y = ambiente.positions[agente.nome]
        # Devolve apenas as células adjacentes e se são paredes/obstáculos
        adjacentes = {
            "UP": (x, y-1) in getattr(ambiente, 'walls', []),
            "DOWN": (x, y+1) in getattr(ambiente, 'walls', []),
            "LEFT": (x-1, y) in getattr(ambiente, 'walls', []),
            "RIGHT": (x+1, y) in getattr(ambiente, 'walls', [])
        }
        return adjacentes

class ProximitySensor(Sensor):
    # Detecta se há paredes nas direções adjacentes
    def ler(self, ambiente, agente):
        x, y = ambiente.positions[agente.nome]
        # Verifica se as células vizinhas estão na lista de paredes do ambiente
        walls = getattr(ambiente, 'walls', set())
        return {
            "wall_up": (x, y-1) in walls or y-1 < 0,
            "wall_down": (x, y+1) in walls or y+1 >= ambiente.height,
            "wall_left": (x-1, y) in walls or x-1 < 0,
            "wall_right": (x+1, y) in walls or x+1 >= ambiente.width
        }