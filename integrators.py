import numpy as np

class VelocityVerlet(object):
    def __init__(self, timestep, system):
        self.timestep = timestep
        self.system = system

    def step(self, x_0, v_0):
        f_0 = self.system.force(x_0) / self.system.mass
        x_1 = x_0 + v_0 * self.timestep + 0.5 * f_0 * self.timestep * self.timestep
        f_1 = self.system.force(x_1) / self.system.mass
        v_1 = v_0 + 0.5 * (f_0 + f_1) * self.timestep

        return x_1, v_1, f_1

    def to_json(self):
        return { "integrator" : "velocity verlet",
                 "timestep" : self.timestep }

class AnalyticalHarmonicOscillator(object):
    def __init__(self, system, x_0, v_0):
        self.system = system
        self._solve_constants(x_0, v_0)

    def _solve_constants(self, x_0, v_0):
        # If phi = k * pi / 2  where k is an integer not equal to 0, we will get a divide by 0
        self.phi = np.arctan2( - v_0 / (self.system.omega * self.system.omega), x_0)
        self.A = x_0 / (self.system.mass * np.cos(self.phi))

    def evaluate_at(self, t):
        common = self.A * self.system.mass
        x =  common * np.cos(self.system.omega * t + self.phi)
        v = - common * self.system.omega * np.sin(self.system.omega * t + self.phi)

        return x, v

    def to_json(self):
        return { "integrator" : "analytical harmonic oscillator",
                 "timestep" : self.timestep }
        

