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

def plot(flname, durations, avg_energies, std_energies, analytical_energies):
    avg_energies = np.array(avg_energies)
    std_energies = np.array(std_energies)

    plt.clf()
    plt.hold(True)
    plt.fill_between(durations,
                     avg_energies + std_energies,
                     avg_energies - std_energies,
                     facecolor="k",
                     alpha=0.5)
    plt.plot(durations,
             avg_energies,
             "k.-",
             label="VV")
    plt.semilogx(durations,
                 [analytical_energies] * len(durations),
                 "m.-",
                 label="Analytical")
    
    plt.xlim([0.0, max(durations) + 0.01])
    plt.legend(loc="upper right")
    plt.xlabel("Simulation Length (s)", fontsize=16)
    plt.ylabel("Energy (J)", fontsize=16)
    plt.title("Average Energy ($\pm$ 1 $\sigma$)", fontsize=18)
    plt.savefig(flname, DPI=300)

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--timestep",
                        type=float,
                        help="Timesteps (in sec)")

    parser.add_argument("--durations",
                        default=100.0,
                        nargs="+",
                        type=float,
                        help="Simulation lengths (in sec) to evaluate")

    parser.add_argument("--plot-fl",
                        type=str,
                        default=None,
                        help="Filename for generated plot")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseargs()

    durations = list(sorted(args.durations))
    avg_energies = []
    std_energies = []
    init_energy = 0
    for dur in durations:
        obs = TotalEnergyObserver(args.timestep)
        simulate_vv(args.timestep, dur, [obs])
        init_energy = obs.energies[0]
        avg_energy, std_energy = obs.stats()
        avg_energies.append(avg_energy)
        std_energies.append(std_energy)
        print dur, init_energy, avg_energy, std_energy

    if args.plot_fl is not None:
        plot(args.plot_fl, durations, avg_energies, std_energies, init_energy)
