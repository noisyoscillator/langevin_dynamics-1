# -*- coding: utf-8 -*-
# Main code for a simple langevin dynamics simulation

# import packages
import matplotlib
matplotlib.use('TkAgg')
import threading
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
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

    def init_plot(self,):
        color = cm.rainbow(np.linspace(0, 1, self.np))
        fig, ax = plt.subplots(1, 1)
        ax.set_xlim(0, range_x)
        ax.set_ylim(0, range_y)
        return color, fig, ax

    def draw_plot(self, ax, x, y, col):
        ax.scatter(x, y, c=col)
        #fig.canvas.restore_region(background)
        #fig.draw_artist(ax)
        #fig.canvas.blit(ax.bbox)
        plt.pause(1e-6)

    def init_force(self, out, fig, ax, color):
        f_tot_x = np.empty(self.np)
        f_tot_y = np.empty(self.np)
        curr_pot = np.empty(self.np)
        for i in range(self.np):
            f_tot_x[i], f_tot_y[i], curr_pot[i] =\
                fe.update_force(self.velx[i], self.vely[i], self.posx[i], self.posy[i])
            self.write_out(out, i + 1, 0, self.posx[i], self.posy[i], self.velx[i], self.vely[i], curr_pot[i])
            #ax.scatter(self.posx[i], self.posy[i], c=color[i])
        #fig.canvas.draw()
        #plt.ion()
        return f_tot_x, f_tot_y, curr_pot

    def dynamics(self, nsteps, f_tot_x, f_tot_y, curr_pot, m, dt, range_x, range_y, out, ax, color):
        def velocity_verlet(tid, niter, n_threads):
            for i in range(niter):
                j = i*n_threads + tid
                if j > self.np - 1:
                    pass
                else:
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
        # initialization
        # begin the loop over all steps
        # using velocity verlet for dynamics
        n_threads = 4
        if self.np % n_threads == 0:
            niter = self.np // n_threads
        else:
            niter = self.np//n_threads + 1

        for i in range(nsteps):
            tid = 0
            for j in range(n_threads):
                t = threading.Thread(target=velocity_verlet, args=(tid, niter, n_threads))
                t.start()
                tid += 1
            t.join()
            for j in range(self.np):
                self.write_out(out, j + 1, i+1, self.posx[j], self.posy[j], self.velx[j], self.vely[j], curr_pot[j])
                #self.draw_plot(ax, self.posx[j], self.posy[j], color[j])
        out.close()
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
# alias for force evaluation function
fe = ForceEval(lam, T, arr_x, arr_y, d_x, d_y, n_y, k_pot, k_fx, k_fy, pot, fx, fy)
# alias for dynamics function
lan = LangevinDynamics(n_p, pos_x, pos_y, vel_x, vel_y)
output = lan.create_out()
color, fig, ax = lan.init_plot()
f_tot_x, f_tot_y, curr_pot = lan.init_force(output, fig, ax, color)
lan.dynamics(N, f_tot_x, f_tot_y, curr_pot, m, dt, range_x, range_y, output, ax, color)
print(time.time() - tstart)
