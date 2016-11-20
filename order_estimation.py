import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("PDF")
import matplotlib.pyplot as plt

if __name__ == "__main__":
    timesteps = np.array([0.1,
                          0.05,
                          0.025,
                          0.01,
                          0.005,
                          0.0025,
                          0.001])

    avg_local_pos_error = np.array([0.02623153722,
                                    0.003287155951,
                                    0.0004111489105,
                                    2.63E-05,
                                    3.29E-06,
                                    4.11E-07,
                                    2.63E-08])

    avg_local_vel_error = np.array([0.08734682373,
                                    0.01060538765,
                                    0.001300412672,
                                    8.28E-05,
                                    1.03E-05,
                                    1.29E-06,
                                    8.27E-08])

    max_global_pos_error = np.array([1.999996042,
                                     1.925578275,
                                     0.6346311748,
                                     0.1030791043,
                                     0.02577397522,
                                     0.006443626148,
                                     0.001030963096])

    max_global_vel_error = np.array([11.94019129,
                                     12.03171521,
                                     3.990773601,
                                     0.6491622412,
                                     0.1623304312,
                                     0.04058671379,
                                     0.006493957821])
                                     

    log_timesteps = np.log(timesteps)
    log_avg_local_pos_error = np.log(avg_local_pos_error)
    log_avg_local_vel_error = np.log(avg_local_vel_error)
    log_max_global_pos_error = np.log(max_global_pos_error)
    log_max_global_vel_error = np.log(max_global_vel_error)

    avg_pos_error_slope, _, avg_pos_error_r, _, _ = stats.linregress(log_timesteps,
                                                                     log_avg_local_pos_error)

    avg_vel_error_slope, _, avg_vel_error_r, _, _ = stats.linregress(log_timesteps,
                                                                     log_avg_local_vel_error)

    max_pos_error_slope, max_pos_error_inter, max_pos_error_r, _, _ = stats.linregress(log_timesteps,
                                                                     log_max_global_pos_error)

    max_vel_error_slope, max_vel_error_inter, max_vel_error_r, _, _ = stats.linregress(log_timesteps,
                                                                     log_max_global_vel_error)

    print "Local Position Error Slope:", avg_pos_error_slope
    print "Local Position Error r^2:", (avg_pos_error_r * avg_pos_error_r)

    print "Local Velocity Error Slope:", avg_vel_error_slope
    print "Local Velocity Error r^2:", (avg_vel_error_r * avg_vel_error_r)

    print "Global Position Error Slope:", max_pos_error_slope
    print "Global Position Error r^2:", (max_pos_error_r * max_pos_error_r)

    print "Global Velocity Error Slope:", max_vel_error_slope
    print "Global Velocity Error r^2:", (max_vel_error_r * max_vel_error_r)

    plt.clf()
    plt.hold(True)
    plt.plot(log_timesteps, log_max_global_pos_error, "c-")
    plt.plot(log_timesteps, max_pos_error_slope * log_timesteps + max_pos_error_inter, "k-")
    plt.xlabel("Time (log s)", fontsize=16)
    plt.ylabel("Max Error (log m/s)", fontsize=16)
    plt.title("Global Position Error", fontsize=18)
    plt.savefig("figures/global_position_error_dt.png", DPI=300)

    max_pos_error_slope, max_pos_error_inter, max_pos_error_r, _, _ = stats.linregress(log_timesteps[2:],
                                                                                       log_max_global_pos_error[2:])

    print "Global Position Error (Truncated) Slope:", max_pos_error_slope
    print "Global Position Error (Truncated) r^2:", (max_pos_error_r * max_pos_error_r)

    plt.clf()
    plt.hold(True)
    plt.plot(log_timesteps, log_max_global_pos_error, "c-", label="Actual")
    plt.plot(log_timesteps, max_pos_error_slope * log_timesteps + max_pos_error_inter, "k-", label="Estimate")
    plt.xlabel("Time (log s)", fontsize=16)
    plt.ylabel("Max Error (log m)", fontsize=16)
    plt.title("Global Position Error", fontsize=18)
    plt.legend(loc="lower right")
    plt.savefig("figures/global_position_error_dt_truncated.png", DPI=300)

    max_vel_error_slope, max_vel_error_inter, max_vel_error_r, _, _ = stats.linregress(log_timesteps[2:],
                                                                                       log_max_global_vel_error[2:])

    print "Global Velocity Error (Truncated) Slope:", max_vel_error_slope
    print "Global Velocity Error (Truncated) r^2:", (max_vel_error_r * max_vel_error_r)

    plt.clf()
    plt.hold(True)
    plt.plot(log_timesteps, log_max_global_pos_error, "c-", label="Actual")
    plt.plot(log_timesteps, max_pos_error_slope * log_timesteps + max_pos_error_inter, "k-", label="Estimate")
    plt.xlabel("Time (log s)", fontsize=16)
    plt.ylabel("Max Error (log m/s)", fontsize=16)
    plt.title("Global Velocity Error", fontsize=18)
    plt.legend(loc="lower right")
    plt.savefig("figures/global_velocity_error_dt_truncated.png", DPI=300)
