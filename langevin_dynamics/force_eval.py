# functions to evaluate force
import numpy as np
from random import gauss


class ForceEval:

    def __init__(self, lam, temp):
        self.lam = lam
        self.T = temp

    def friction(self, v):
        """
        solvent drag force
        :param v:
        :return:
        """
        f_drag = -self.lam*v
        return f_drag

    def ran_force(self):
        # calculate standard deviation of noise
        sigma = np.sqrt(2*np.sqrt(self.lam)*self.T)
        # generate random noise
        f_ran = gauss(0, sigma)
        return f_ran

    def pot_force(self, x, y):
        pass


