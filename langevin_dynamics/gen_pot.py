# functions related to external potential
# either generating new file or reading from the old file
# a 2D sin wave is used here
# z = c*sin(a*x**2 + b*y**2)

import numpy as np
import os

class GeneratePotential:

    def __init__(self, arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c):
        self.arr_x = arr_x
        self.arr_y = arr_y
        self.nx = len(arr_x)
        self.ny = len(arr_y)
        size = self.nx*self.ny
        self.pot = np.empty(size)
        self.fx = np.empty(size)
        self.fy = np.empty(size)
        self.x = range_x
        self.y = range_y
        self.dx = d_x
        self.dy = d_y
        self.a = a
        self.b = b
        self.c = c

    def gen_pot(self):
        pot_file = os.path.isfile('potential.txt')
        if pot_file:
            self.chk_existing()
        else:
            self.get_new()
        return self.pot, self.fx, self.fy, self.nx, self.ny

    def chk_existing(self):
        pot_param = list(np.genfromtxt('potential.txt', max_rows=1))
        param_arr = [self.x, self.y, self.dx, self.dy, self.a, self.b, self.c]
        if param_arr == pot_param:
            raw_data = np.genfromtxt('potential.txt', usecols=(2, 3, 4), skip_header=3).T
            self.pot = raw_data[0]
            self.fx = raw_data[1]
            self.fy = raw_data[2]
        else:
            self.get_new()


    def ep_fxn(self, var, var1):
        ep = self.c*np.sin(self.a*var**2 + self.b*var1**2)
        return ep

    def force_fxn(self, var, var1, m):
        """
        merge fx and fy calculations together
        :param m: a*x for x direction and b*y for y
        :return: force on that direction
        """
        force_p = 2*self.c*m*np.cos(self.a*var**2 + self.b*var1**2)
        return force_p

    def get_new(self):
        output = open('potential.txt', 'w')
        print('# Parameters used to generate this potential file are\n'
              '# x range, y range, delta x, delta y, c, a and b, respectively\n'
              '{} {} {} {} {} {} {}\n# index position potential force\n'
              .format(self.x, self.y, self.dx, self.dy, self.a, self.b, self.c), file=output)
        c_x = self.x/2
        c_y = self.y/2
        for i in range(self.nx):
            for j in range(self.ny):
                ind = i*self.nx+j
                tmp = self.arr_x[i] - c_x
                tmp1 = self.arr_y[j] - c_y
                self.pot[ind] = self.ep_fxn(tmp, tmp1)
                self.fx[ind] = self.force_fxn(tmp, tmp1, self.a*tmp)
                self.fy[ind] = self.force_fxn(tmp, tmp1, self.b*tmp1)
                print('{:6.2f}{:6.2f}{:13.7f}{:13.7f}{:13.7f}'
                      .format(self.arr_x[i], self.arr_y[j], self.pot[ind], self.fx[ind], self.fy[ind]), file=output)
        output.close()
