from src.agentes.base import AgenteBase

def direction_to_target(pos, target):
    x, y = pos
    tx, ty = target

    if x < tx: return "RIGHT"
    if x > tx: return "LEFT"
    if y < ty: return "DOWN"
    if y > ty: return "UP"
    return "STAY"

class FixedAgent(AgenteBase):
    def age(self):
        pos = self.current_obs["self_pos"]
        target = self.current_obs["target"]
        return direction_to_target(pos, target)
