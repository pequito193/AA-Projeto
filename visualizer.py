import matplotlib.pyplot as plt

class Visualizador:
    def __init__(self):
        plt.ion()  # Liga o modo interativo do matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

    def desenhar(self, ambiente, agentes, ep, step):
        self.ax.clear() # Limpa o frame anterior
        
        # Configuração do Grid
        self.ax.set_xlim(-0.5, ambiente.width - 0.5)
        self.ax.set_ylim(-0.5, ambiente.height - 0.5)
        self.ax.set_title(f"Episódio: {ep} | Passo: {step}")
        self.ax.grid(True)

        # Desenhar Paredes (se existirem no ambiente)
        if hasattr(ambiente, 'walls'):
            for wx, wy in ambiente.walls:
                self.ax.add_patch(plt.Rectangle((wx-0.5, wy-0.5), 1, 1, color="black"))

        # Desenhar Alvo (Target)
        tx, ty = ambiente.target
        self.ax.add_patch(plt.Rectangle((tx-0.4, ty-0.4), 0.8, 0.8, color="red", label="Alvo"))

        # Desenhar Agentes
        for name, pos in ambiente.positions.items():
            x, y = pos
            self.ax.plot(x, y, 'bo', markersize=10) # 'bo' = bola azul
            self.ax.text(x, y + 0.3, name, ha="center", fontweight='bold')

        self.ax.set_aspect("equal")
        
        plt.draw()
        plt.pause(0.001) # Pequena pausa para permitir a renderização do novo frame

    def fechar(self):
        plt.ioff()
        plt.show()