===============================
langevin_dynamics
===============================

In statistical physics, a Langevin equation (Paul Langevin, 1908) is a stochastic differential 
equation describing the time evolution of a subset of the degrees of freedom. 

.. image:: https://img.shields.io/pypi/v/langevin_dynamics.svg
        :target: https://pypi.python.org/pypi/langevin_dynamics

.. image:: https://img.shields.io/travis/tautomer/langevin_dynamics.svg
        :target: https://travis-ci.org/tautomer/langevin_dynamics

.. image:: https://coveralls.io/repos/github/tautomer/langevin_dynamics/badge.svg?branch=master
        :target: https://coveralls.io/github/tautomer/langevin_dynamics?branch=master

.. image:: https://readthedocs.org/projects/langevin-dynamics/badge/?version=latest
        :target: https://langevin-dynamics.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tautomer/langevin_dynamics/shield.svg
     :target: https://pyup.io/repos/github/tautomer/langevin_dynamics/
     :alt: Updates


Python Boilerplate contains all the boilerplate you need to create a Python package.


* Free software: MIT license
* Documentation: https://langevin-dynamics.readthedocs.io.


Features
--------

* A simple python program for Lagevin equation simulation.

* Required input values are read from a file named input and output file is called trajectory.txt.

* Potential is based on simply y = c[b-a(x-d)\ :sup:`2`\]\ :sup:`2`\, which is a good example of typical
  double well potential in chemistry. You can change a,b and c and the range in gen_pot.py to get your
  own potential file.

* Periodic boundary conditions enabled.

TODO
---------

* Adding a module to convert tracjectories into animation.
* Integration of main code and potential generating code.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

