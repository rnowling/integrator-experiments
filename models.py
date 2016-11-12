class HarmonicOscillator(object):
    def __init__(self, omega, mass):
        self.omega = omega
        self.mass = mass

    def potential_energy(self, x):
        return 0.5 * self.omega * self.omega * self.mass * x * x

    def force(self, x):
        return - self.omega * self.omega * self.mass * x

    def to_json(self):
        return { "system_type" : "harmonic oscillator",
                 "omega" : self.omega,
                 "mass" : self.mass }
