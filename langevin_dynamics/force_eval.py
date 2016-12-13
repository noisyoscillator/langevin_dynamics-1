# functions to evaluate force
import numpy as np
from random import gauss


class ForceEval:

    def __init__(self, lam, temp, arr_x, arr_y, d_x, d_y, n_y, k_pot, k_fx, k_fy, pot, fx, fy):
        self.lam = lam
        self.T = temp
        self.arr_x = arr_x
        self.arr_y = arr_y
        self.dx = d_x
        self.dy = d_y
        self.ny = n_y
        self.kpot = k_pot
        self.kfx = k_fx
        self.kfy = k_fy
        self.pot = pot
        self.fx = fx
        self.fy = fy

    def update_force(self, vx, vy, x, y):
        """
        function to update total force
        :param v: velocity
        :param x: x position
        :param y: y position
        :return: the total force of current particle
        """
        curr_pot, f_p_x, f_p_y = self.pot_force(x, y)
        f_drag_x, f_drag_y = self.friction(vx, vy)
        f_ran_x, f_ran_y = self.ran_force()
        force_x = f_p_x + f_drag_x + f_ran_x
        force_y = f_p_y + f_drag_y + f_ran_y
        return force_x, force_y, curr_pot

    def friction(self, vx, vy):
        """
        solvent drag force
        :param v:
        :return:
        """
        drag_force_x = -self.lam * vx
        drag_force_y = -self.lam * vy
        return drag_force_x, drag_force_y

    def ran_force(self):
        # calculate standard deviation of noise
        sigma = np.sqrt(2*np.sqrt(self.lam)*self.T)
        # generate random noise
        f_ran_x = gauss(0, sigma)
        f_ran_y = gauss(0, sigma)
        return f_ran_x, f_ran_y

    def pot_force(self, x, y):
        ind_x = x // self.dx
        ind_y = y // self.dy
        delta_x = x % self.dx
        delta_y = x % self.dy
        ind_1 = int(ind_x*self.ny + ind_y)
        ind_2 = int((ind_x+1)*self.ny + ind_y)
        ind_k_1 = int(ind_x*(self.ny-1) + ind_y)
        ind_k_2 = int((ind_x+1)*(self.ny-1) + ind_y)
        tmp = [self.kpot[ind_k_1], self.kfx[ind_k_1], self.kfy[ind_k_1]]
        tmp1 = [self.kpot[ind_k_2], self.kfx[ind_k_2], self.kfy[ind_k_2]]
        tmp2 = [self.pot[ind_1], self.fx[ind_1], self.fy[ind_1]]
        tmp3 = [self.pot[ind_2], self.fx[ind_2], self.fy[ind_2]]
        result = [None] * 3
        for i in range(3):
            f_r1 = tmp[i]*delta_y + tmp2[i]
            f_r2 = tmp1[i]*delta_y + tmp3[i]
            result[i] = (f_r2-f_r1)/self.dx*delta_x + f_r1
        curr_pot = result[0]
        f_p_x = result[1]
        f_p_y = result[2]
        return curr_pot, f_p_x, f_p_y
