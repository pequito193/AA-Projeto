import csv

class Logger:
    def __init__(self):
        self.rows = []

    def registar(self, ep, agent, reward, steps):
        self.rows.append((ep, agent, reward, steps))

    def guardar(self, filename):
        with open(filename, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["episode", "agent", "reward", "steps"])
            w.writerows(self.rows)
