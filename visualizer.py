import matplotlib.pyplot as plt

class Visualizador:
    def desenhar(self, ambiente, agentes):
        fig, ax = plt.subplots(figsize=(5,5))

        ax.set_xlim(-0.5, ambiente.width - 0.5)
        ax.set_ylim(-0.5, ambiente.height - 0.5)
        ax.grid(True)

        # target
        tx, ty = ambiente.target
        ax.add_patch(plt.Rectangle((tx-0.4, ty-0.4), 0.8, 0.8, color="red"))

        for name, pos in ambiente.positions.items():
            x, y = pos
            ax.text(x, y, name, ha="center", va="center")

        ax.set_aspect("equal")
        ax.invert_yaxis()
        plt.show()
