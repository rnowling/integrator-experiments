import argparse

import numpy as np

from common import write_system
from models import HarmonicOscillator
from integrators import AnalyticalHarmonicOscillator

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output-fl",
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

    system = HarmonicOscillator(omega, mass)
    integrator = AnalyticalHarmonicOscillator(delta_t, system)

    xs, vs, ts = integrator.simulate(steps, x_0, v_0)

    xs = np.array(xs)
    vs = np.array(vs)
    ts = np.array(ts)

    ke = 0.5 * mass * vs * vs
    pe = 0.5 * mass * omega * omega * xs * xs
    total_energy = ke + pe

    print "Average total energy:", np.mean(total_energy)
    print "Std total energy:", np.std(total_energy)

    if args.output_fl:
        write_system(args.output_fl,
                     integrator,
                     (ts, xs, vs))

    

    
    

    
    
