import argparse

import numpy as np

from common import write_system
from models import HarmonicOscillator
from integrators import AnalyticalHarmonicOscillator

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output-fl",
                        type=str)

    parser.add_argument("--steps",
                        default=1000,
                        type=int,
                        help="Number of steps")

    parser.add_argument("--dt",
                        default=0.01,
                        type=float,
                        help="Time step")

    return parser.parse_args()

if __name__ == "__main__":
    args = parseargs()
    
    omega = 2 * np.pi # rad / sec
    mass = 2 # kg
    x_0 = 1 # m
    v_0 = 0 # m / s

    system = HarmonicOscillator(omega, mass)
    integrator = AnalyticalHarmonicOscillator(system, x_0, v_0)

    xs = []
    vs = []
    ts = []
    for i in xrange(args.steps):
        t = args.dt * i
        x, v = integrator.evaluate_at(t)
        xs.append(x)
        vs.append(v)
        ts.append(t)

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

    

    
    

    
    
