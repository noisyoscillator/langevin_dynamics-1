#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_langevin_dynamics
----------------------------------

Tests for `langevin_dynamics` module.
"""


import unittest
import subprocess
import numpy as np
import os
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
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
    def test_init_dyn(self):
        arr_x = [0, 1]
        arr_y = [0, 1]
        range_x = 1
        range_y = 1
        d_x = 1
        d_y = 1
        a = 1
        b = 1
        c = 1
        n_p = 1
        T = 1
        m = 1
        pot, fx, fy, n_x, n_y, pos_x, pos_y, vel_x, vel_y, k_pot, k_fx, k_fy\
            = self.iv.init_dyn(arr_x, arr_y, range_x, range_y, d_x, d_y, a, b, c, n_p, T, m)
        self.assertEqual(np.sin(0.5), pot[0])
