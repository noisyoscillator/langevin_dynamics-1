# functions related to external potential
# either generating new file or reading from the old file
# a 2D sin wave is used here
# z = c*sin(a*x**2 + b*y**2)

import numpy as np
import os
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))


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
        self.pot_file_path = dir_root + '/potential.txt'

    def gen_pot(self):
        """
        unify reading and generating potential file
        :return:
        """
        # check f potential file exists
        pot_file = os.path.isfile(self.pot_file_path)
        if pot_file:
            # if exists, go to check
            self.chk_existing()
        else:
            # if not, re-generate
            self.get_new()
        return self.pot, self.fx, self.fy, self.nx, self.ny

    def chk_existing(self):
        # read the parameters to generate potential file from the file
        pot_param = list(np.genfromtxt(self.pot_file_path, max_rows=1))
        # write current ones to a list
        param_arr = [self.x, self.y, self.dx, self.dy, self.a, self.b, self.c]
        # compare (by the virtue of lists)
        if param_arr == pot_param:
            # if same, read and assign
            raw_data = np.genfromtxt(self.pot_file_path, usecols=(2, 3, 4), skip_header=3).T
            self.pot = raw_data[0]
            self.fx = raw_data[1]
            self.fy = raw_data[2]
        else:
            # if not, re-generate it
            self.get_new()

    def ep_fxn(self, var, var1):
        """
        function for potential
        :param var: x
        :param var1: y
        :return:
        """
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
        output = open(self.pot_file_path, 'w')
        print('# Parameters used to generate this potential file are\n'
              '# x range, y range, delta x, delta y, c, a and b, respectively\n'
              '{} {} {} {} {} {} {}\n# index position potential force\n'
              .format(self.x, self.y, self.dx, self.dy, self.a, self.b, self.c), file=output)
        # keep the center of potential in the middle
        c_x = self.x/2
        c_y = self.y/2
        # loop over number of x
        for i in range(self.nx):
            # loop over y
            for j in range(self.ny):
                # index
                ind = i*self.nx+j
                # move x and y
                tmp = self.arr_x[i] - c_x
                tmp1 = self.arr_y[j] - c_y
                # calculate potential and forces
                self.pot[ind] = self.ep_fxn(tmp, tmp1)
                self.fx[ind] = self.force_fxn(tmp, tmp1, self.a*tmp)
                self.fy[ind] = self.force_fxn(tmp, tmp1, self.b*tmp1)
                # write
                print('{:6.2f}{:6.2f}{:13.7f}{:13.7f}{:13.7f}'
                      .format(self.arr_x[i], self.arr_y[j], self.pot[ind], self.fx[ind], self.fy[ind]), file=output)
        output.close()
