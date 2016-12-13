# -*- coding: utf-8 -*-
# Main code for a simple langevin dynamics simulation

# import packages
import numpy as np
# solve path problem
import sys
import os
# get source file directory so that the program can be executable from anywhere
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(dir_root)
from initialization import InitValues
from force_eval import ForceEval


class LangevinDynamics():

    def __init__(self, n_p, pos_x, pos_y, vel_x, vel_y):
        self.np = n_p
        self.posx = pos_x
        self.posy = pos_y
        self.velx = vel_x
        self.vely = vel_y
        pass

    def create_out(self):
        # open output file
        out = open('trajectory.txt', 'w')
        # write header
        print('# output file for Langevin dynamics simulation\n'
              '# n_p   n_steps   position_x    position_y    velocity_x    velocity_y    curr_potential\n', file=out)
        return out

    def write_out(self, out, i_par, n_steps, position_x, position_y, velocity_x, velocity_y, currpot):
        print('{:5d} {:7d} {:13.7f} {:13.7f} {:13.7f} {:13.7f}  {:13.7f}'.
              format(i_par, n_steps, position_x, position_y, velocity_x, velocity_y, currpot), file=out)

    def init_force(self, out):
        f_tot_x = np.empty(self.np)
        f_tot_y = np.empty(self.np)
        curr_pot = np.empty(self.np)
        for i in range(self.np):
            f_tot_x[i], f_tot_y[i], curr_pot[i] =\
                fe.update_force(self.velx[i], self.vely[i], self.posx[i], self.posy[i])
            self.write_out(out, i + 1, 0, self.posx[i], self.posy[i], self.velx[i], self.vely[i], curr_pot[i])
        return f_tot_x, f_tot_y, curr_pot

    def dynamics(self, nsteps, f_tot_x, f_tot_y, curr_pot, m, dt, range_x, range_y, out):
        # initialization
        # begin the loop over all steps
        # using velocity verlet for dynamics
        for i in range(nsteps):
            for j in range(self.np):
                # calculate accelerations for both direction
                a_x = f_tot_x[j] / m
                a_y = f_tot_y[j] / m
                # update half-step velocity for x and y
                self.velx[j] += 0.5 * a_x * dt
                self.vely[j] += 0.5 * a_y * dt
                # update position for both x and y
                self.posx[j] += self.velx[j] * dt
                self.posy[j] += self.vely[j] * dt
                # apply PBC
                self.posx[j] %= range_x
                self.posy[j] %= range_y
                # update force
                f_tot_x[j], f_tot_y[j], curr_pot[j] =\
                    fe.update_force(self.velx[j], self.vely[j], self.posx[j], self.posy[j])
                # calculate accelerations for both direction
                a_x = f_tot_x[j] / m
                a_y = f_tot_y[j] / m
                # update half-step velocity for x and y
                self.velx[j] += 0.5 * a_x * dt
                self.vely[j] += 0.5 * a_y * dt
                # write output
                self.write_out(out, j + 1, i+1, self.posx[j], self.posy[j], self.velx[j], self.vely[j], curr_pot[j])
        out.close()

a = 1
b = 1
c = 1
switch = 1
# short form of the class
iv = InitValues()
# Initialization for all necessary quantities
range_x, range_y, d_x, d_y, n_p, dt, m, lam, N, T, arr_x, arr_y = iv.read_input()
pot, fx, fy, n_x, n_y, pos_x, pos_y, vel_x, vel_y, k_pot, k_fx, k_fy\
    = iv.init_dyn(arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c, n_p, T, m)
# alias for force evaluation function
fe = ForceEval(lam, T, arr_x, arr_y, d_x, d_y, n_y, k_pot, k_fx, k_fy, pot, fx, fy)
# alias for dynamics function
lan = LangevinDynamics(n_p, pos_x, pos_y, vel_x, vel_y)
output = lan.create_out()
f_tot_x, f_tot_y, curr_pot = lan.init_force(output)
lan.dynamics(N, f_tot_x, f_tot_y, curr_pot, m, dt, range_x, range_y, output)
