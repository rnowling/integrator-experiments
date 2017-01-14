import copy

import numpy as np

class State(object):
    def __init__(self):
        self.positions = None
        self.velocities = None
        self.momenta = None
        self.forces = None
        self.simulated_time = None
        self.kinetic_energy = None
        self.potential_energy = None
        self.total_energy = None

    def copy(self):
        return copy.deepcopy(self)

class HarmonicOscillator(object):
    def __init__(self, omega, mass, initial_positions, initial_velocities):
        self.omega = omega
        self.mass = mass
        self.initial_positions = initial_positions
        self.initial_velocities = initial_velocities

    def init_state(self):
        state = State()
        state.positions = self.initial_positions
        state.velocities = self.initial_velocities
        state.momenta = self.mass * self.initial_velocities
        state.simulated_time = 0.0
        self.update_energies(state)

        return state

    def update_energies(self, state):
        state.forces = self.force(state)
        state.kinetic_energy = self.kinetic_energy(state)
        state.potential_energy = self.potential_energy(state)
        state.total_energy = state.kinetic_energy + state.potential_energy

        return state
        
    def potential_energy(self, state):
        return 0.5 * self.omega * self.omega * self.mass * state.positions * state.positions

    def force(self, state):
        f = - self.omega * self.omega * self.mass * state.positions
        return f

    def kinetic_energy(self, state):
        return 0.5 * self.mass * state.velocities * state.velocities
        
    def to_json(self):
        return { "system_type" : "harmonic oscillator",
                 "omega" : self.omega,
                 "mass" : self.mass }
