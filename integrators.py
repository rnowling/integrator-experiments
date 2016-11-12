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

