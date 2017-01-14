import argparse

import numpy as np

from common import write_system
from models import HarmonicOscillator
from integrators import VelocityVerlet
from integrators import AnalyticalHarmonicOscillator

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--output-fl",
                        type=str)

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
    t_0 = 0.0

    system = HarmonicOscillator(omega, mass)
    integrator = VelocityVerlet(args.dt, system)
    analytical = AnalyticalHarmonicOscillator(system, x_0, v_0)

    xs = [x_0]
    vs = [v_0]
    ts = [t_0]
    analytical_xs = [x_0]
    analytical_vs = [v_0]
    for i in xrange(args.steps):
        x_0, v_0, _ = integrator.step(x_0, v_0)
        t_0 += args.dt
        a_x, a_v  = analytical.evaluate_at(t_0)
        xs.append(x_0)
        vs.append(v_0)
        ts.append(t_0)
        analytical_xs.append(a_x)
        analytical_vs.append(a_v)

    xs = np.array(xs)
    vs = np.array(vs)
    ts = np.array(ts)
    analytical_xs = np.array(analytical_xs)
    analytical_vs = np.array(analytical_vs)

    grad_xs = -1. * np.array([system.force(x) for x in xs])
    conf_ke = 0.5 * xs * grad_xs
    ke = 0.5 * mass * vs * vs
    pe = 0.5 * mass * omega * omega * xs * xs
    total_energy = ke + pe
    total_conf_energy = conf_ke + pe

    anal_grad_xs = -1. * np.array([system.force(x) for x in analytical_xs])
    anal_conf_ke = 0.5 * analytical_xs * anal_grad_xs
    anal_ke = 0.5 * mass * analytical_vs * analytical_vs
    anal_pe = 0.5 * mass * omega * omega * analytical_xs * analytical_xs
    anal_total_energy = anal_ke + anal_pe
    anal_conf_energy = anal_conf_ke + anal_pe

    print "Average total energy:", np.mean(total_energy)
    print "Std total energy:", np.std(total_energy)
    print
    print "Average KE energy:", np.mean(ke)
    print "Std KE energy:", np.std(ke)
    print
    print "Average total conf energy:", np.mean(total_conf_energy)
    print "Std total conf energy:", np.std(total_conf_energy)
    print
    print "Average Conf Energy:", np.mean(conf_ke)
    print "Std Conf Energy:", np.std(conf_ke)
    print

    print "Average total energy:", np.mean(anal_total_energy)
    print "Std total energy:", np.std(anal_total_energy)
    print
    print "Average KE energy:", np.mean(anal_ke)
    print "Std KE energy:", np.std(anal_ke)
    print
    print "Average total conf energy:", np.mean(anal_conf_energy)
    print "Std total conf energy:", np.std(anal_conf_energy)
    print
    print "Average Conf Energy:", np.mean(anal_conf_ke)
    print "Std Conf Energy:", np.std(anal_conf_ke)
    print
    

    if args.output_fl:
        write_system(args.output_fl,
                     integrator,
                     (ts, xs, vs))


    

    
    

    
    
