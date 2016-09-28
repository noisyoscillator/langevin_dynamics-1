#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_langevin_dynamics
----------------------------------

Tests for `langevin_dynamics` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from langevin_dynamics.main import langevin_dynamics
from langevin_dynamics import gen_pot
from langevin_dynamics import cli



class TestLangevin_dynamics(unittest.TestCase):

    def setUp(self):
        self.lan = langevin_dynamics()

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_assignvalue(self):
        param = [ 1,2,3,4,5,6,7 ]
        test = self.lan.assignvalue(param)
        self.assertEqual(test,1)

    def test_initialization(self):
        test = self.lan.initialization()
        self.assertEqual(test,0)

    def test_fileopen(self):
        test = self.lan.create_out()
        value = "<_io.TextIOWrapper name='trajectory.txt' mode='w' encoding='UTF-8'>"
        self.assertEqual(value,str(test))



#    def test_command_line_interface(self):
#        runner = CliRunner()
#        result = runner.invoke(cli.main)
#        assert result.exit_code == 0
#        assert 'langevin_dynamics.cli.main' in result.output
#        help_result = runner.invoke(cli.main, ['--help'])
#        assert help_result.exit_code == 0
#        assert '--help  Show this message and exit.' in help_result.output
#
#
#if __name__ == '__main__':
#    sys.exit(unittest.main())
if __name__ == '__main__':
    sys.exit(unittest.main())
