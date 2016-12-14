# -*- coding: utf-8 -*-
# Main code for a simple langevin dynamics simulation

# import packages
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
import time
# solve path problem
import sys
import os
# get source file directory so that the program can be executable from anywhere
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(dir_root)
from initialization import InitValues
from force_eval import ForceEval


class LangevinDynamics():

    def __init__(self, n_p, range_x, range_y, pos_x, pos_y, vel_x, vel_y, f_tot_x, f_tot_y, curr_pot, dt, m):
        self.np = n_p
        self.x = range_x
        self.y =range_y
        self.posx = pos_x
        self.posy = pos_y
        self.velx = vel_x
        self.vely = vel_y
        self.f_x = f_tot_x
        self.f_y = f_tot_y
        self.pot = curr_pot
        self.dt = dt
        self.m = m
        pass

    def write_out(self, out, i_par, n_steps, position_x, position_y, velocity_x, velocity_y, currpot):
        print('{:5d} {:7d} {:13.7f} {:13.7f} {:13.7f} {:13.7f}  {:13.7f}'.
              format(i_par, n_steps, position_x, position_y, velocity_x, velocity_y, currpot), file=out)

    def draw_plot(self, ax, x, y, col):
        ax.scatter(x, y, c=col)
        #fig.canvas.restore_region(background)
        #fig.draw_artist(ax)
        #fig.canvas.blit(ax.bbox)
        plt.pause(1e-6)

    def dynamics(self, nsteps, out, ax, color):
        # initialization
        # begin the loop over all steps
        # using velocity verlet for dynamics
        for i in range(nsteps):
            print(i)
            if __name__ == '__main__':
                with Pool(None) as p:
                    result = np.asarray(p.map(self.velocity_verlet, list(range(self.np)))).T
                self.velx = result[0]
                self.vely = result[1]
                self.posx = result[2]
                self.posy = result[3]
                self.f_x = result[4]
                self.f_y = result[5]
                self.pot = result[6]
            for j in range(self.np):
                self.write_out(out, j + 1, i+1, self.posx[j], self.posy[j], self.velx[j], self.vely[j], self.pot[j])
        out.close()

    def velocity_verlet(self, j):
        # calculate accelerations for both direction
        a_x = self.f_x[j] / self.m
        a_y = self.f_y[j] / self.m
        # update half-step velocity for x and y
        self.velx[j] += 0.5 * a_x * self.dt
        self.vely[j] += 0.5 * a_y * self.dt
        # update position for both x and y
        self.posx[j] += self.velx[j] * self.dt
        self.posy[j] += self.vely[j] * self.dt
        # apply PBC
        self.posx[j] %= self.x
        self.posy[j] %= self.y
        # update force
        self.f_x[j], self.f_y[j], self.pot[j] =\
            fe.update_force(self.velx[j], self.vely[j], self.posx[j], self.posy[j])
        # calculate accelerations for both direction
        a_x = self.f_x[j] / self.m
        a_y = self.f_y[j] / self.m
        # update half-step velocity for x and y
        self.velx[j] = self.velx[j] + 0.5 * a_x * self.dt
        self.vely[j] += 0.5 * a_y * self.dt
        return self.velx[j], self.vely[j], self.posx[j], self.posy[j], self.f_x[j], self.f_y[j], self.pot[j]
        # write output

        #self.draw_plot(ax, self.posx[j], self.posy[j], color[j])
tstart = time.time()
a = 0.5
b = 0.5
c = 0.5
# short form of the class
iv = InitValues()
# Initialization for all necessary quantities
range_x, range_y, d_x, d_y, n_p, dt, m, lam, N, T, arr_x, arr_y = iv.read_input()
pot, fx, fy, n_x, n_y, pos_x, pos_y, vel_x, vel_y, k_pot, k_fx, k_fy\
    = iv.init_dyn(arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c, n_p, T, m)
output = iv.create_out()
color, fig, ax = iv.init_plot(n_p, range_x, range_y)
# alias for force evaluation function
fe = ForceEval(lam, T, arr_x, arr_y, d_x, d_y, n_y, k_pot, k_fx, k_fy, pot, fx, fy)
f_tot_x, f_tot_y, curr_pot = fe.init_force(output, n_p, vel_x, vel_y, pos_x, pos_y, fig, ax, color)
# alias for dynamics function
lan = LangevinDynamics(n_p, range_x, range_y, pos_x, pos_y, vel_x, vel_y, f_tot_x, f_tot_y, curr_pot, dt, m)
lan.dynamics(N, output, ax, color)
print(time.time() - tstart)
