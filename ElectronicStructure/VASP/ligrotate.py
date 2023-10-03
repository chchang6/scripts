#!/usr/bin/env python
# Script to convert POSCAR file to Cartesians.

import numpy
import sys
from re import search
from math import cos, sin, radians

# User definitions
# Following string specifies ligand atoms. Format 'range1, range2, ...'. Convert to 1-indexed list
lig_atoms_string = '1-5'
# Number of theta grid points, including theta=0
num_theta_points = 10
# Number of phi grid points, including phi=0
num_phi_points = 11

t = lig_atoms_string.split(',')
lig_atoms = []
for i in t:
   if search('-', i):
      t2 = i.split('-')
      lig_atoms.extend([j for j in range(int(t2[0]), int(t2[1])+1)])

# Open POSCAR file
file = open('POSCAR', 'r')
data = file.readlines()
file.close()

# Transformation matrix should be on lines 3-5
row0 = [float(i) for i in data[2].strip().split()]
row1 = [float(i) for i in data[3].strip().split()]
row2 = [float(i) for i in data[4].strip().split()]
F2C = numpy.matrix([row0, row1, row2]).T
C2F = F2C.I

# Coordinates start from line 10 (1-indexed).
#   Grab lines for ligand atoms, pack into matrix
ref_fracs = numpy.zeros((3,len(lig_atoms)), numpy.float)
refline = 8
for i in xrange(len(lig_atoms)):
   t = [float(j) for j in data[refline+lig_atoms[i]].split()[0:3]]
   ref_fracs[:,i] = t
frac_coors = numpy.asmatrix(ref_fracs)
ref_carts = F2C * frac_coors

# Now need to generate rotated ligand according to grids specified above.
# First calculate center. Don't bother mass-weighting
center = numpy.mean(ref_carts, axis=1)
translated = ref_carts - center

# Create dictionary with keys (theta, phi). Assume that theta and phi values will be
#   integral in degree units.
coordict = {}
theta_increment = 180 / (num_theta_points-1)
phi_increment = 360 / (num_phi_points-1)
# Rotate about theta; assume RH coordinate system (x out, y right). Rotate RH around y
for i in xrange(num_theta_points):
   theta = i * theta_increment
   Rtheta = numpy.matrix([ [cos(radians(float(theta))), 0., sin(radians(float(theta)))], \
                           [0., 1., 0.], \
                           [-sin(radians(float(theta))), 0., cos(radians(float(theta)))] ])
   theta_coors = Rtheta * translated
   # Rotate these around z axis by phi
   for j in xrange(num_phi_points-1):  # Don't need the 360 deg point
      phi = j * phi_increment
      Rphi = numpy.matrix([ [cos(radians(float(phi))), -sin(radians(float(phi))), 0.], \
                            [sin(radians(float(phi))), cos(radians(float(phi))), 0.], \
                            [0., 0., 1.] ])
      phi_coors = Rphi * theta_coors
      trans_phi_coors = phi_coors + center
      frac_trans_phi_coors = C2F * trans_phi_coors
      coordict[(theta,phi)] = frac_trans_phi_coors

# Go through dictionary and replace the ligand lines with rotated fractional coordinates.
lig_atom_lines = [refline + i for i in lig_atoms]
for i in coordict.keys():
   file = open('POSCAR-' + str(i[0]) + '-' + str(i[1]), 'w')
   ligatom_number = 0
   for j in xrange(len(data)):
      if j in lig_atom_lines:
         file.write('%20.16f%20.16f%20.16f   T   T   T\n' % (coordict[i][0,ligatom_number], \
         coordict[i][1,ligatom_number], coordict[i][2,ligatom_number]))
         ligatom_number += 1
      else:
         file.write(data[j])
   file.close()

