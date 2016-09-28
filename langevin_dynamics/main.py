# -*- coding: utf-8 -*-
# Main code for a simple langevin dynamics simulation

# import packages
import math
import numpy
import random

class langevin_dynamics():

    def __init__(self):
        self.x = 0
        self.v = 0
        self.dt = 0
        self.m = 0
        self.lam = 0
        self.N = 0
        self.T = 0

    def assignvalue(self,param):

        # I figure this is useful for the program
        # but I cannot get 100% coverage with if

        #number_types = (int, float)
        #for i in (0,len(param)-1):
        #  if isinstance(param[i], number_types):
        #      continue
        #  else:
        #        raise ValueError
        #  initial position
        self.x = param[0]
        # initial velocity
        self.v = param[1]
        # time step interval
        self.dt = param[2]
        # mass
        self.m = param[3]
        # solvent drag force coefficient
        self.lam = param[4]
        # total number of steps
        self.N = int(param[5])
        # temperature
        self.T = param[6]
        # for unittest purpose
        return self.x

    def create_out(self):
        # open output file
        self.out = open('trajectory.txt','w')
        # write header
        self.out.write('# output file for langevin dynamcis simulation\n# index  time     postion    velocity  energy\n')
        return self.out

    def write_out(self,index,time,posistion,velocity,energy):
        print('{:5d} {:8.3f} {:10.5f} {:12.7f}{:12.7f}'.format(index,time,posistion,velocity,energy),file=self.out)

    def initialization(self):
        # assign initial values
        self.assignvalue(param)
        # initial solvent drag force
        self.fs = -self.lam*self.v
        # calculate standard deviation of noise
        self.sigma = math.sqrt(2*math.sqrt(self.lam)*self.T)
        # generate random noise
        self.fn = random.gauss(0,self.sigma)
        # initial potential force
        self.ref, self.energy, self.force = pot[:, 1:].T
        self.pos_list = list(self.ref)
        # apply periodic boundary conditions
        self.L = max(self.pos_list)
        self.x = self.x%self.L
        # end of PBC
        # round to 3 decimals
        self.pos = round(self.x,3)
        self.index = self.pos_list.index(self.pos)
        self.fp = self.force[self.index]
        self.p = self.energy[self.index]
        self.e = 0.5*self.m*self.v**2 + self.p
        # calculate accelaretion
        self.a = (self.fs-self.fp+self.fn)/self.m
        # for unittest purpose
        return self.fs

    def dynamics(self):
        # initialization
        self.initialization()
        self.create_out()
        self.write_out(0,0.000,self.x,self.v,self.e)
        # begin the loop over all steps
        # using velocity verlet for dynamics
        for i in range(0,self.N):
            # update half-step velocity
            self.v = self.v + 0.5*self.a*self.dt
            # update position
            self.x = self.x + self.v*self.dt
            # update force
            self.fn = random.gauss(0,self.sigma)
            self.fs = -self.lam*self.v
            self.x = self.x%self.L
            self.pos = round(self.x,3)
            self.index = self.pos_list.index(self.pos)
            self.fp = self.force[self.index]
            self.p = self.energy[self.index]
            self.a = (self.fs-self.fp+self.fn)/self.m
            # update another half step velocity
            self.v = self.v + 0.5*self.a*self.dt
            self.e = 0.5*self.m*self.v**2 + self.p
            # write output
            self.write_out(i+1,self.dt*(i+1),self.x,self.v,self.e)
        self.out.close()

# short form of the class
lan = langevin_dynamics()
# read input file
param = numpy.loadtxt('input',comments='#')
# read for potential energy file
pot = numpy.loadtxt('potential.txt',comments='#')
# run dynamics
lan.dynamics()

