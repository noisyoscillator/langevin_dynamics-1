# -*- coding: utf-8 -*-
# Main code for a simple langevin dynamics simulation

# import packages
import math
import numpy
import random

# a stupid way of reading input quantities
lines = [line.rstrip('\n') for line in open('input')]
# initial position
x = float(lines[1])
# initial velocity
v = float(lines[3])
# time step interval
dt = float(lines[5])
# mass
m = float(lines[7])
# solvent drag force coefficient
lam = float(lines[9])
# total number of steps
N = int(lines[11])
# temperature
T = float(lines[13])

# initial solvent drag force
fs = -lam*v
# calculate standard deviation of noise
sigma = math.sqrt(2*math.sqrt(lam)*T)
# generate random noise
fn = random.gauss(0,sigma)
# initial potential force
# read for potential energy file
pot = numpy.loadtxt('potential.txt')
ref, energy, force = pot[:, 1:].T
pos_list = list(ref)
# round to 3 decimals
pos = round(x,3)
index = pos_list.index(pos)
fp = force[index]
# to get potential energy
p = energy[index]
# calculate accelaretion
a = (fs-fp+fn)/m
# a = -fp/m # uesd to check energy conserving

# end of initialization

# open output file
out = open('tracjectory.txt','w')
out.write('# output file for langevin dynamcis simulation\n# index time postion velocity\n')
# print initial postion
print('{:4} {:6} {:7.3f} {:11.7f} {:11.7f}'.format('0','0.00',x,v,p),file=out)

# begin the loop over all steps
# using velocity verlet for dynamics
for i in range(0,N):
    # update half-step velocity
    v = v + 0.5*a*dt
    # update position
    x = x + v*dt
    # update force
    fn = random.gauss(0,sigma)
    fs = -lam*v
    pos = round(x,3)
    index = pos_list.index(pos)
    fp = force[index]
    p = energy[index]
    a = (fs-fp+fn)/m
#    a = -fp/m #   for testing purpose
    # update another half step velocity
    v = v + 0.5*a*dt
    # to calculate total energy
    e = 0.5*m*v**2 + p
    # write output
    print('{:4d} {:6.3f} {:7.3f} {:11.7f} {:11.7f}'.format(i+1,dt*(i+1),x,v,e),file=out)
out.close()


