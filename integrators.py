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
    def __init__(self, timestep, system):
        self.timestep = timestep
        self.system = system

    def simulate(self, steps, x_0, v_0):
        phi, A = self.system.solve_analytical(x_0, v_0)

        ts = np.arange(steps) * self.timestep
        xs = A * self.system.mass * np.cos(self.system.omega * ts + phi)
        vs = - A * self.system.mass * self.system.omega * np.sin(self.system.omega * ts + phi)

        return xs, vs, ts

    def to_json(self):
        return { "integrator" : "analytical harmonic oscillator",
                 "timestep" : self.timestep }
        

