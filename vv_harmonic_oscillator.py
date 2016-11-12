import argparse

import numpy as np

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

from common import write_system
from models import HarmonicOscillator
from integrators import VelocityVerlet

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output-fl",
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

    write_system(args.output_fl,
                 integrator,
                 (ts, xs, vs))


    

    
    

    
    
