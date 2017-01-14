import argparse

import numpy as np

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

from observers import TotalEnergyObserver
from models import HarmonicOscillator
from integrators import VelocityVerlet
from integrators import AnalyticalHarmonicOscillator

def simulate_vv(dt, duration, observers):
    omega = 2 * np.pi # rad / sec
    mass = 2 # kg
    x_0 = 1 # m
    v_0 = 0 # m / s
    t_0 = 0.0

    model = HarmonicOscillator(omega, mass, x_0, v_0)
    state = model.init_state()
    integrator = VelocityVerlet(dt, model, state)

    for observer in observers:
            observer.observe(state)
            
    while state.simulated_time <= duration:
        state = integrator.step()
        for observer in observers:
            observer.observe(state)

def plot(flname, dts, avg_energies, std_energies, analytical_energies):
    avg_energies = np.array(avg_energies)
    std_energies = np.array(std_energies)

    plt.clf()
    plt.hold(True)
    plt.fill_between(dts,
                     avg_energies + std_energies,
                     avg_energies - std_energies,
                     facecolor="k",
                     alpha=0.5)
    plt.plot(dts,
             avg_energies,
             "k.-",
             label="VV")
    plt.semilogx(dts,
                 [analytical_energies] * len(dts),
                 "m.-",
                 label="Analytical")
    
    plt.xlim([0.0, max(dts) + 0.01])
    plt.legend(loc="lower left")
    plt.xlabel("Timestep (s)", fontsize=16)
    plt.ylabel("Energy (J)", fontsize=16)
    plt.title("Average Energy ($\pm$ 1 $\sigma$)", fontsize=18)
    plt.savefig(flname, DPI=300)

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--timesteps",
                        type=float,
                        nargs="+",
                        help="List of timesteps (in sec) to evaluate")

    parser.add_argument("--duration",
                        default=100.0,
                        type=float,
                        help="Simulation length")

    parser.add_argument("--plot-fl",
                        type=str,
                        default=None,
                        help="Filename for generated plot")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseargs()

    dts = list(sorted(args.timesteps))
    avg_energies = []
    std_energies = []
    init_energy = 0
    period = max(dts)
    for dt in dts:
        obs = TotalEnergyObserver(period)
        simulate_vv(dt, args.duration, [obs])
        init_energy = obs.energies[0]
        avg_energy, std_energy = obs.stats()
        avg_energies.append(avg_energy)
        std_energies.append(std_energy)
        print dt, init_energy, avg_energy, std_energy

    if args.plot_fl is not None:
        plot(args.plot_fl, dts, avg_energies, std_energies, init_energy)
