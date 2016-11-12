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

if __name__ == "__main__":
    args = parseargs()
    
    steps = 1000
    delta_t = 0.01 # sec
    omega = 2 * np.pi # rad / sec
    mass = 2 # kg
    x_0 = 1 # m
    v_0 = 0 # m / s

    phi = np.arctan2( - v_0 / (omega * omega), x_0)
    # If phi = k * pi / 2  where k is an integer not equal to 0, we will get a divide by 0
    A = x_0 / (mass * np.cos(phi))

    print "phi", phi
    print "A", A

    ts = np.arange(steps) * delta_t
    xs = A * mass * np.cos(omega * ts + phi)
    vs = - A * mass * omega * np.sin(omega * ts + phi)
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

    

    
    

    
    
