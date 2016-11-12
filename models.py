import numpy as np

class HarmonicOscillator(object):
    def __init__(self, omega, mass):
        self.omega = omega
        self.mass = mass

    def potential_energy(self, x):
        return 0.5 * self.omega * self.omega * self.mass * x * x

    def force(self, x):
        return - self.omega * self.omega * self.mass * x

    def solve_analytical(self, x_0, v_0):
        # If phi = k * pi / 2  where k is an integer not equal to 0, we will get a divide by 0
        phi = np.arctan2( - v_0 / (self.omega * self.omega), x_0)
        A = x_0 / (self.mass * np.cos(phi))

        return phi, A

    def to_json(self):
        return { "system_type" : "harmonic oscillator",
                 "omega" : self.omega,
                 "mass" : self.mass }
