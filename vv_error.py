import argparse

import numpy as np

from models import HarmonicOscillator
from integrators import VelocityVerlet
from integrators import AnalyticalHarmonicOscillator

from scipy.stats import linregress

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

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
    analytical_integrator = AnalyticalHarmonicOscillator(system, x_0, v_0)

    local_error_xs = []
    local_error_vs = []
    global_error_xs = []
    global_error_vs = []
    ts = []
    t = 0.0
    analytical_x = x_0
    analytical_v = v_0
    global_vv_x = x_0
    global_vv_v = v_0
    for i in xrange(args.steps):
        t = args.dt * (i + 1)
        local_vv_x, local_vv_v, _ = vv_integrator.step(analytical_x, analytical_v)
        global_vv_x, global_vv_v, _ = vv_integrator.step(global_vv_x, global_vv_v)
        analytical_x, analytical_v = analytical_integrator.evaluate_at(t)
        local_error_x = np.abs(analytical_x - local_vv_x)
        local_error_v = np.abs(analytical_v - local_vv_v)
        global_error_x = np.abs(analytical_x - global_vv_x)
        global_error_v = np.abs(analytical_v - global_vv_v)

        local_error_xs.append(local_error_x)
        local_error_vs.append(local_error_v)
        global_error_xs.append(global_error_x)
        global_error_vs.append(global_error_v)

        ts.append(t)

    local_error_xs = np.array(local_error_xs)
    local_error_vs = np.array(local_error_vs)
    global_error_xs = np.array(global_error_xs)
    global_error_vs = np.array(global_error_vs)
    ts = np.array(ts)

    print "Average local position error:", np.mean(local_error_xs)
    print "Std local position error:", np.std(local_error_xs)
    print "Average local velocity error:", np.mean(local_error_vs)
    print "Std local velocity error:", np.std(local_error_vs)
    print

    max_cum_error_xs = []
    max_cum_error_vs = []
    max_error_xs = 0.0
    max_error_vs = 0.0
    for i in xrange(len(global_error_xs)):
        max_error_xs = max(global_error_xs[i], max_error_xs)
        max_error_vs = max(global_error_vs[i], max_error_vs)
        max_cum_error_xs.append(max_error_xs)
        max_cum_error_vs.append(max_error_vs)

    # max_error = c * elapsed_time + b    
    max_slope, max_intercept, max_r, _, _ = linregress(ts, max_cum_error_xs)
    print "Max global position error:", max(max_cum_error_xs)
    print "Max global position error slope:", max_slope
    print "Max global position error r^2:", (max_r * max_r)
    plt.clf()
    plt.hold(True)
    plt.plot(ts, global_error_xs, "c-")
    plt.plot(ts, max_slope * ts + max_intercept, "k-")
    plt.xlabel("Time (s)", fontsize=16)
    plt.ylabel("Error (m)", fontsize=16)
    plt.title("Global Position Error", fontsize=18)
    plt.ylim([0, max(max(max_slope * ts + max_intercept), max(max_cum_error_xs))])
    plt.savefig("figures/global_position_error.png", DPI=300)

    
    max_slope, max_intercept, max_r, _, _ = linregress(ts, max_cum_error_vs)
    print "Max global velocity error:", max(max_cum_error_vs)
    print "Max global velocity error slope:", max_slope
    print "Max global velocity error r^2:", (max_r * max_r)
    plt.clf()
    plt.hold(True)
    plt.plot(ts, global_error_vs, "c-")
    plt.plot(ts, max_slope * ts + max_intercept, "k-")
    plt.xlabel("Time (s)", fontsize=16)
    plt.ylabel("Error (m/s)", fontsize=16)
    plt.title("Global Velocity Error", fontsize=18)
    plt.ylim([0, max(max(max_slope * ts + max_intercept), max(max_cum_error_vs))])
    plt.savefig("figures/global_velocity_error.png", DPI=300)
