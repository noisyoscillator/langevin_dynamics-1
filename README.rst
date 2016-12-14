===============================
langevin_dynamics
===============================

In statistical physics, a Langevin equation (Paul Langevin, 1908) is a stochastic differential 
equation describing the time evolution of a subset of the degrees of freedom.

.. image:: https://img.shields.io/travis/tautomer/langevin_dynamics.svg?branch=master
        :target: https://travis-ci.org/tautomer/langevin_dynamics

.. image:: https://coveralls.io/repos/github/tautomer/langevin_dynamics/badge.svg?branch=master
        :target: https://coveralls.io/github/tautomer/langevin_dynamics?branch=master

.. image:: https://readthedocs.org/projects/langevindynamics/badge/?version=latest
        :target: http://langevindynamics.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python Boilerplate contains all the boilerplate you need to create a Python package.


* Free software: MIT license
* Documentation: https://langevindynamics.readthedocs.io.


Features
--------

* A simple python program for 2D many-particle Lagevin equation simulation.

* Required input values are read from a file named input and output file is called trajectory.txt.

* Potential is based on simply y = c*sin (a*x\ :sup:`2`\ + b*y\ :sup:`2`\), which may not be physical at all.
  You can change a,b and c in main program to get your
  own potential file.

* Periodic boundary conditions enabled.

* Paralleled main dynamics loop

* Real-time display is added to the program. (Note: cause the program to become really slow.)

* For more information please check langevin_dynamics.info.

Note
----

* Please modify input under langevin_dynamcis folder before running simulations.

TODO
---------

* Adding a module to convert tracjectories into gif to avoid performance issue.
* Including more physical potentials, such as Lennard-Jones potential.
* Re-structure the code to use higher level parallelism, and may introduce C/Fortran implementation for heavy computations.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

