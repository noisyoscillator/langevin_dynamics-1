# keep for future use
# move all initialization to this file

import numpy as np

class InitValues:

    def __init__(self):
        pass

    def read_input(self):
        raw_data = np.genfromtxt('input', dtype=np.float32)
        #  initial position
        x = raw_data[0]
        # initial velocity
        v = raw_data[1]
        # time step interval
        dt = raw_data[2]
        # mass
        m = raw_data[3]
        # solvent drag force coefficient
        lam = raw_data[4]
        # total number of steps
        N = int(raw_data[5])
        # temperature
        T = raw_data[6]
        return x, v, dt, m, lam, N, T

    def grid_interp(self):
        pass

iv = InitValues()
