import argparse

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

import numpy as np

from common import read_system

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--trajectory-fl",
                        required=True,
                        type=str)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--phase-fl", type=str)
    group.add_argument("--energy-fl", type=str)

    return parser.parse_args()

def plot_phase(flname, xs, vs):
    plt.clf()
    plt.plot(xs, vs)
    plt.xlabel("Position", fontsize=16)
    plt.ylabel("Velocity", fontsize=16)
    plt.title("Phase Diagram", fontsize=18)
    plt.savefig(flname, DPI=300)

def plot_energy(flname, ts, ke, pe):
    total_energy = ke + pe

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
    plt.savefig(flname, DPI=300)

if __name__ == "__main__":
    args = parseargs()

    simulation = read_system(args.trajectory_fl)

    trajectory = simulation["trajectory"]
    xs = np.array(trajectory["positions"])
    vs = np.array(trajectory["velocities"])
    ts = np.array(trajectory["time"])

    if args.phase_fl:
        plot_phase(args.phase_fl, xs, vs)
    elif args.energy_fl:
        mass = simulation["system"]["mass"]
        omega = simulation["system"]["omega"]
        
        ke = 0.5 * mass * vs * vs
        pe = 0.5 * mass * omega * omega * xs * xs

        plot_energy(args.energy_fl, ts, ke, pe)

    
    
