import numpy as np

class TotalEnergyObserver(object):
    def __init__(self, period):
        self.period = period
        self.energies = []
        self.eps = 1e-5

    def observe(self, state):
        if state.simulated_time % self.period < self.eps:
            self.energies.append(state.total_energy)

    def stats(self):
        return np.mean(self.energies), np.std(self.energies)
