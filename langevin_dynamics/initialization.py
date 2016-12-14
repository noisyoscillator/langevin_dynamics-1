# keep for future use
# move all initialization to this file

import numpy as np
import random
# solve path problem
import sys
import os
# get source file directory so that the program can be executable from anywhere
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(dir_root)
from gen_pot import GeneratePotential


class InitValues:

    def __init__(self):
        pass

    def read_input(self):
        # make sure to read from the dir of the source code
        inp_file = dir_root + '/input'
        raw_data = np.genfromtxt(inp_file, dtype=np.float32)
        # x range
        x = raw_data[0]
        # y range
        y = raw_data[1]
        # resolution on x axis
        d_x = raw_data[2]
        # resolution on y axis
        d_y = raw_data[3]
        # number of particles
        n_p = int(raw_data[4])
        # time step interval
        dt = raw_data[5]
        # mass
        m = raw_data[6]
        # solvent drag force coefficient
        lam = raw_data[7]
        # total number of steps
        N = int(raw_data[8])
        # temperature
        T = raw_data[9]
        arr_x = np.arange(0, x+d_x, d_x)
        arr_y = np.arange(0, y+d_y, d_y)
        return x, y, d_x, d_y, n_p, dt, m, lam, N, T, arr_x, arr_y

    def init_dyn(self, arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c, n_p, temp, m):
        """
        get initial values for dynamics
        :param arr_x: x array
        :param arr_y: y array
        :param range_x:
        :param range_y:
        :param d_x: x resolution
        :param d_y: y resolution
        :param a:
        :param b:
        :param c:
        :param n_p:
        :param temp: temperature
        :param m: mass
        :return:
        """
        # call potential function
        gp = GeneratePotential(arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c)
        # get potential, force and numbers of grid
        pot, fx, fy, n_x, n_y = gp.gen_pot()
        # assign initial positions
        pos_x, pos_y = self.assgin_pos(range_x, range_y, n_p)
        # assign initial velocities
        vel_x, vel_y = self.assign_vel(n_p, temp, m)
        # get slopes for interpolation
        k_pot, k_fx, k_fy = self.grid_interp(pot, fx, fy, n_x, n_y, d_y)
        return pot, fx, fy, n_x, n_y, pos_x, pos_y, vel_x, vel_y, k_pot, k_fx, k_fy

    def assgin_pos(self, range_x, range_y, n_p):
        """
        random uniform distribution of initial positions
        :param range_x:
        :param range_y:
        :param n_p:
        :return:
        """
        # n_p random integers
        pos_x = np.asarray(random.sample(range(0, int(100*n_p)), n_p))
        # get a random number
        tmp1 = random.uniform(0, 1)
        # keep position in the range of x and looks "very random"
        pos_x %= range_x - tmp1
        # same procedure for y
        pos_y = np.asarray(random.sample(range(0, int(100*n_p)), n_p))
        tmp1 = random.uniform(0, 1)
        pos_y %= range_y - tmp1
        return pos_x, pos_y

    def assign_vel(self, n_p, t, m):
        """
        assign velocities by Gaussian distribution
        :param n_p:
        :param t: temperature
        :param m: mass
        :return:
        """
        sigma = np.sqrt(t/m)
        vel_x = [random.gauss(0, sigma) for _ in range(n_p)]
        vel_y = [random.gauss(0, sigma) for _ in range(n_p)]
        return vel_x, vel_y

    def grid_interp(self, pot, fx, fy, n_x, n_y, dy):
        """
        get the slope of grid on y direction
        :param pot: potential array
        :param fx: x force array
        :param fy:
        :param n_x:
        :param n_y:
        :param dy: resolution on y direction
        :return: slopes on y for potential and force
        """
        # size of slope array
        size = n_x * (n_y-1)
        k_pot = np.empty(size)
        k_fx = np.empty(size)
        k_fy = np.empty(size)
        for i in range(n_x):
            tmp = i * n_y
            for j in range(n_y-1):
                # index for y values
                ind = tmp + j
                # index for slopes
                ind_k = ind - i
                k_pot[ind_k] = pot[ind + 1] - pot[ind]
                k_fx[ind_k] = fx[ind + 1] - fx[ind]
                k_fy[ind_k] = fy[ind + 1] - fy[ind]
        # divide by d_y
        k_pot /= dy
        k_fx /= dy
        k_fy /= dy
        return k_pot, k_fx, k_fy
