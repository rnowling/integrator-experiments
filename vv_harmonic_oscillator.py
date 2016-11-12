import argparse

import numpy as np

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--phase-fl",
                        required=True,
                        type=str)

    parser.add_argument("--energy-fl",
                        required=True,
                        type=str)

    return parser.parse_args()

class HarmonicOscillator(object):
    def __init__(self, omega, mass):
        self.omega = omega
        self.mass = mass

    def potential_energy(self, x):
        return 0.5 * self.omega * self.omega * self.mass * x * x

    def force(self, x):
        return - self.omega * self.omega * self.mass * x

class VelocityVerlet(object):
    def __init__(self, timestep, system):
        self.timestep = timestep
        self.system = system

    def step(self, x_0, v_0):
        f_0 = self.system.force(x_0) / system.mass
        x_1 = x_0 + v_0 * self.timestep + 0.5 * f_0 * self.timestep * self.timestep
        f_1 = self.system.force(x_1) / system.mass
        v_1 = v_0 + 0.5 * (f_0 + f_1) * self.timestep

        return x_1, v_1, f_1

if __name__ == "__main__":
    args = parseargs()
    
    steps = 1000
    delta_t = 0.01 # sec
    omega = 2 * np.pi # rad / sec
    mass = 2 # kg
    x_0 = 1 # m
    v_0 = 0 # m / s
    t_0 = 0.0

    system = HarmonicOscillator(omega, mass)
    integrator = VelocityVerlet(delta_t, system)

    xs = [x_0]
    vs = [v_0]
    ts = [t_0]
    for i in xrange(steps):
        x_0, v_0, _ = integrator.step(x_0, v_0)
        t_0 += delta_t
        xs.append(x_0)
        vs.append(v_0)
        ts.append(t_0)

    ts = np.array(ts)
    vs = np.array(vs)
    xs = np.array(xs)
    
    ke = 0.5 * mass * vs * vs
    pe = 0.5 * mass * omega * omega * xs * xs
    total_energy = ke + pe

    plt.clf()
    plt.plot(xs, vs)
    plt.xlabel("Position", fontsize=16)
    plt.ylabel("Velocity", fontsize=16)
    plt.title("Phase Diagram", fontsize=18)
    plt.savefig(args.phase_fl, DPI=300)

    plt.clf()
    plt.plot(ts, ke, "c-", label="Kinetic")
    plt.plot(ts, pe, "m-", label="Potential")
    plt.plot(ts, total_energy, "k-", label="Total")
    plt.xlabel("Time (sec)", fontsize=16)
    plt.ylabel("Energy (J)", fontsize=16)
    plt.title("System Energy", fontsize=18)
    min_energy = min(min(ke), min(pe), min(total_energy))
    max_energy = max(max(ke), max(pe), max(total_energy))
    plt.ylim([- max_energy * 0.2, max_energy * 1.2])
    plt.legend(loc="lower right")
    plt.savefig(args.energy_fl, DPI=300)

    

    
    

    
    
