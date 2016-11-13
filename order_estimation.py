import numpy as np
from scipy import stats

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

    log_timesteps = np.log(timesteps)
    log_avg_local_pos_error = np.log(avg_local_pos_error)
    log_avg_local_vel_error = np.log(avg_local_vel_error)

    pos_error_slope, _, pos_error_r, _, _ = stats.linregress(log_timesteps,
                                                             log_avg_local_pos_error)

    vel_error_slope, _, vel_error_r, _, _ = stats.linregress(log_timesteps,
                                                             log_avg_local_vel_error)

    print "Position Error Slope:", pos_error_slope
    print "Position Error r^2:", (pos_error_r * pos_error_r)

    print "Velocity Error Slope:", vel_error_slope
    print "Velocity Error r^2:", (vel_error_r * vel_error_r)

    

    
