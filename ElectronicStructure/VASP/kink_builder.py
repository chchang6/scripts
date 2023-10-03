#!/usr/bin/env python
# Script to build kinked surface with 111 terrace, 002 edges, and
#    -111 kinks.

import math
import numpy

# Title for VASP job
VASP_title = 'Pd(111) terrace + (002) step + (-111) kink'

# Define supercell
a = 22.344 # Angstroms
b = 22.344
c = 21.172
alpha = math.radians(60.)
beta = math.radians(90.)
gamma = math.radians(120.)

# Construct Cartesian cell vectors from unit cell parameters
volume = math.sqrt(1. - math.pow(math.cos(alpha),2) - math.pow(math.cos(beta),2) - \
   math.pow(math.cos(gamma),2) + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
T11 = a
T12 = b*math.cos(gamma)
T13 = c*math.cos(beta)
T21 = 0.
T22 = b*math.sin(gamma)
T23 = c*((math.cos(alpha) - math.cos(beta)*math.cos(gamma))/math.sin(gamma))
T31 = 0.
T32 = 0.
T33 = c*volume/math.sin(gamma)

trans = numpy.matrix([ [T11, T12, T13], [T21, T22, T23], [T31, T32, T33] ])

# Fractional coordinate axes are just 1 0 0 etc. in cell coordinate system
a_frac = numpy.matrix( [1., 0., 0.] ).T
b_frac = numpy.matrix( [0., 1., 0.] ).T
c_frac = numpy.matrix( [0., 0., 1.] ).T

# Now express these in Cartesian space with actual cell dimensions
a_cart = trans*a_frac
b_cart = trans*b_frac
c_cart = trans*c_frac

# Define atom spacings based on generator cell. For FCC with 111
#   plane, easiest to use origin + face-centered atoms
spacing1 = 2.793

# Calculate atomic spacing along each axis in fractional units
spacing_a = spacing1/a
spacing_b = spacing1/b
spacing_c = spacing1/c

# Define padding at supercell edges for convenience
pad_a = spacing_a/2.
pad_b = spacing_b/2.

# Creating 4 8X8 planes of Pd. Top layer is 4(b)X8(a) half-layer,
#    plus on 4-atom line along a.
atoms_along_a_base = 8
atoms_along_b_base = 8
basal_layers = 4
atoms_top_step = 4  # Defines half-layer width on top
atoms_along_kink_edge = 4  # Defines length of extra atom line on top

coors = []

# Generate basal layers
for i in xrange(basal_layers):
   for j in xrange(atoms_along_a_base):
      for k in xrange(atoms_along_b_base):
         atom_c = i * spacing_c
         atom_a = j * spacing_a + pad_a
         atom_b = k * spacing_b + pad_b
         coors.append([atom_a, atom_b, atom_c])

# Generate top half-plane
for i in xrange(atoms_along_a_base):
   for j in xrange(atoms_top_step):  # Half along b
      atom_a = i * spacing_a + pad_a
      atom_b = j * spacing_b + pad_b
      atom_c = basal_layers * spacing_c
      coors.append([atom_a, atom_b, atom_c])

# Generate extra line for kink
for i in xrange(atoms_along_kink_edge):
   atom_a = i * spacing_a + pad_a
   atom_b = atoms_top_step * spacing_b + pad_b
   atom_c = basal_layers * spacing_c
   coors.append([atom_a, atom_b, atom_c])

atomtypes = ['Pd']
atomcounts = [len(coors)]

# Write out POSCAR file
file = open('POSCAR', 'w')
file.write(VASP_title + '\n')
file.write('%19.14f\n' % (1.0))
file.write('  %21.16f%21.16f%21.16f\n' % (a_cart[0,0], a_cart[1,0], a_cart[2,0]) )
file.write('  %21.16f%21.16f%21.16f\n' % (b_cart[0,0], b_cart[1,0], b_cart[2,0]) )
file.write('  %21.16f%21.16f%21.16f\n' % (c_cart[0,0], c_cart[1,0], c_cart[2,0]) )
for i in atomtypes:
   file.write('   %-2s' % (i))
file.write('\n')
for i in atomcounts:
   file.write('%4i' % (i))
file.write('\n')
file.write('Selective dynamics\n')
file.write('Direct\n')
for i in coors:
   file.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (i[0], i[1], i[2], 'T', 'T', 'T'))
file.write('\n')
for i in xrange(len(coors)):
   file.write('%16.8E%16.8E%16.8E\n' % (0., 0., 0.))
file.close()
