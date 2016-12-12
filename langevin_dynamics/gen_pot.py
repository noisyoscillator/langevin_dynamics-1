# functions related to external potential
# either generating new file or reading from the old file
# a 2D sin wave is used here
# z = c*sin(a*x**2 + b*y**2)

import numpy as np
import os

class GeneratePotential:

    def __init__(self, range_x, range_y, d_x, a, b, c):
        self.arr_x = np.arange(0, range_x+d_x, d_x)
        self.arr_y = np.arange(0, range_y+d_x, d_x)
        self.n = len(self.arr_x)
        self.c_x = range_x/2
        self.c_y = range_y/2

    def gen_pot(self):
        pot_file = os.system('find potential.txt')
        if pot_file:
            self.chk_existing()
        else:
            self.get_new()


    def chk_existing(self):
        pot_param = list(np.genfromtxt('potential.txt', max_rows=1))
        param_arr = [range_x, range_y, a, b, c]
        if param_arr == pot_param:
            raw_data = np.genfromtxt('potential.txt', usecols=(2, 3, 4), skip_header=3).T
            pot = raw_data[0]
            fx = raw_data[1]
            fy = raw_data[2]
            return pot, fx, fy
        else:
            self.get_new()

    def ep_fxn(self, x, y):
        print(a)
        ep = c*np.sin(a*x**2 + b*y**2)
        return ep

    def force_fxn(self, x, y, m):
        """
        merge fx and fy calculations together
        :param m: a*x for x direction and b*y for y
        :return: force on that direction
        """
        force_p = 2*c*x*m*np.cos(a*x**2 + b*y**2)
        return force_p

    def get_new(self):
        output = open('potential.txt', 'w')
        print('# Parameters used to generate this potential file are\n'
              '# x range, y range, c, a and b, respectively\n'
              '{} {} {} {} {}\n# index position potential force\n'.format(range_x, range_y, a, b, c), file=output)
        size = self.n**2
        pot = np.empty(size)
        fx = np.empty(size)
        fy = np.empty(size)
        for i in range(self.n):
            for j in range(self.n):
                ind = i*self.n+j
                tmp = self.arr_x[i] - self.c_x
                tmp1 = self.arr_y[j] - self.c_y
                pot[ind] = self.ep_fxn(tmp, tmp1)
                fx[ind] = self.force_fxn(tmp, tmp1, a*tmp)
                fy[ind] = self.force_fxn(tmp, tmp1, b*tmp1)
                print('{:5.2f}{:5.2f}{:11.7f}{:11.7f}{:11.7f}'
                      .format(self.arr_x[i], self.arr_y[j], pot[ind], fx[ind], fy[ind]), file=output)
        output.close()
        return pot, fx, fy

range_x = 1
range_y = 1
d_x = 0.01
c = 2
a = 1
b = 1

gp = GeneratePotential(range_x, range_y, d_x, a, b, c)
#gp.get_new()
#gp.gen_pot()
gp.ep_fxn(1, 1)


