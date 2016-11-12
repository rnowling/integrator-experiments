import argparse

import numpy as np

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

from common import write_system
from models import HarmonicOscillator
from integrators import AnalyticalHarmonicOscillator

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

    system = HarmonicOscillator(omega, mass)
    integrator = AnalyticalHarmonicOscillator(delta_t, system)

    xs, vs, ts = integrator.simulate(steps, x_0, v_0)

    write_system(args.output_fl,
                 integrator,
                 (ts, xs, vs))

    

    
    

    
    
