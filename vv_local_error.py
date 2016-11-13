import argparse

import numpy as np

from models import HarmonicOscillator
from integrators import VelocityVerlet
from integrators import AnalyticalHarmonicOscillator

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dt",
                        default=0.01,
                        type=float,
                        help="Timestep in seconds")

    parser.add_argument("--steps",
                        default=1000,
                        type=int,
                        help="Number of steps to simulate for")

    return parser.parse_args()


if __name__ == "__main__":
    args = parseargs()
    
    omega = 2 * np.pi # rad / sec
    mass = 2 # kg
    x_0 = 1 # m
    v_0 = 0 # m / s

    system = HarmonicOscillator(omega, mass)
    vv_integrator = VelocityVerlet(args.dt, system)
    analytical_integrator = AnalyticalHarmonicOscillator(args.dt, system)

    error_xs = []
    error_vs = []
    ts = []
    t = 0.0
    analytical_x = x_0
    analytical_v = v_0
    for i in xrange(args.steps):
        t = args.dt * (i + 1)
        vv_x, vv_v, _ = vv_integrator.step(analytical_x, analytical_v)
        analytical_x, analytical_v = analytical_integrator.evaluate_at(t, x_0, v_0)
        error_x = np.abs(analytical_x - vv_x)
        error_v = np.abs(analytical_v - vv_v)

        error_xs.append(error_x)
        error_vs.append(error_v)
        ts.append(t)

    error_xs = np.array(error_xs)
    error_vs = np.array(error_vs)
    ts = np.array(ts)

    print "Average local position error:", np.mean(error_xs)
    print "Std local position error:", np.std(error_xs)
    print "Average local velocity error:", np.mean(error_vs)
    print "Std local velocity error:", np.std(error_vs)
