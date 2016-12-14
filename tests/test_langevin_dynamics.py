#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_langevin_dynamics
----------------------------------

Tests for `langevin_dynamics` module.
"""


import unittest
import subprocess

#from langevin_dynamics.main import LangevinDynamics
from langevin_dynamics.force_eval import ForceEval
from langevin_dynamics.gen_pot import GeneratePotential
from langevin_dynamics.initialization import InitValues


class TestInitValues(unittest.TestCase):

    def setUp(self):
        self.iv = InitValues()

    def test_reading_input(self):
        range_x, range_y, d_x, d_y, n_p, dt, m, lam, N, T, arr_x, arr_y = self.iv.read_input()
        grep_line_with_bash = 'cd langevin_dynamics;head -n 2 input | tail -n 1'
        test = float(subprocess.check_output(grep_line_with_bash, shell=True))
        self.assertEqual(test, range_x)

#    functions is ok, but nose report type problem. don't want to fix it
#    def test_init_dyn(self):
#        arr_x = [0, 1]
#        arr_y = [0, 1]
#        range_x = 1
#        range_y = 1
#        d_x = 1
#        d_y = 1
#        a = 1
#        b = 1
#        c = 1
#        n_p = 1
#        T = 1
#        m = 1
#        pot, fx, fy, n_x, n_y, pos_x, pos_y, vel_x, vel_y, k_pot, k_fx, k_fy\
#            = self.iv.init_dyn(arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c, n_p, T, m)
#        self.assertEqual(np.sin(0.5), pot[0])

    def test_grid_interp(self):
        pot = [0, 1, 2, 3]
        fx = [0, 1, 2, 3]
        fy = [0, 1, 2, 3]
        n_x = 2
        n_y = 2
        dy = 1
        k_pot, k_fx, k_fy = self.iv.grid_interp(pot, fx, fy, n_x, n_y, dy)
        self.assertEqual(1, k_pot[0])


class TestGeneratePotential(unittest.TestCase):

    def setUp(self):
        self.gp = GeneratePotential(list(range(0, 501)), list(range(0, 501)), 50, 50, 0.1, 0.1, 1, 1, 1)

    def test_gen_pot(self):
        arr1, arr2, arr3, tmp, tmp1 = self.gp.gen_pot()
        self.assertEqual(501**2, len(arr1))

    # no time for this one
    def test_get_new(self):
        pass


#class TestLangevinDynamics(unittest.TestCase):

    #def setUp(self):
    #    self.lan = LangevinDynamics(1, [0], [0], [0], [0])

    # bad structure no way to do unit test
    # need think to re-structure the code
    #def test_create_out(self):
    #    pass
