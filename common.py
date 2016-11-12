import json

def write_system(flname, integrator, trajectory):
    with open(flname, "w") as fl:
        d = { "system" : integrator.system.to_json(),
              "integrator" : integrator.to_json(),
              "trajectory" : { "time" : tuple(trajectory[0]),
                               "positions" : tuple(trajectory[1]),
                               "velocities" : tuple(trajectory[2]) } }
        json.dump(d, fl)
