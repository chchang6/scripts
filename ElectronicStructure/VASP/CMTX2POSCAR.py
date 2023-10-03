#!/usr/bin/env python
# Script to convert Crystalmaker CMTX file to VASP POSCAR file
# CHC 022613
# CHC 032213 Modify to handle FCC cell output from Crystalmaker

import re, math
import numpy

RE1 = re.compile('CELL')
RE2 = re.compile('ATOM')
RE3 = re.compile('LATC')

# User data
CMTX_file = 'Pd.cmtx'
VASP_title = 'Pd cell to optimize lattice constant'

file = open(CMTX_file, 'r')
data = file.readlines()
file.close()

face_centered = False
# Get relevant information from input data.
for i in data:
   if RE3.match(i):
      t = i.rstrip().split()
      if t[1] == 'F': face_centered = True
   elif RE1.match(i):
      t = i.strip().split()
      [a,b,c] = [float(j) for j in t[1:4]]
      [alpha,beta,gamma] = [math.radians(float(j)) for j in t[4:]]
   elif RE2.match(i):
      atoms = []
      fracs = []
      refline = data.index(i)
      j = 1
      while True:
         if data[refline + j] == '\n': break
         else:
            temp = data[refline + j].split()
            atoms.append(temp[0])
            fracs.append([float(k) for k in temp[2:5]])
            j += 1

# If cell has symmetry, need to supplement atom list
if face_centered == True:
   for i in xrange(3):
      atoms.append(atoms[-1 - i])  # Will append repetition of last original atom of list
      t = [0.5, 0.5, 0.5]; t[i] = 0.  # Generates fractional coordinates for face atoms
      fracs.append(t)

# Testing
#print 'a = ' + str(a)
#print 'b = ' + str(b)
#print 'c = ' + str(c)
#print 'alpha = ' + str(alpha)
#print 'beta = ' + str(beta)
#print 'gamma = ' + str(gamma)

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

# Testing
#print 'a_cart = '
#print a_cart
#print 'b_cart = '
#print b_cart
#print 'c_cart = '
#print c_cart

# Get count of atomtypes
atomtypes = []
for i in atoms:
   if i not in atomtypes: atomtypes.append(i)
atomcounts = [ atoms.count(i) for i in atomtypes ]

# Write out output data
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
for i in fracs:
   file.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (i[0], i[1], i[2], 'T', 'T', 'T'))
file.write('\n')
for i in xrange(len(fracs)):
   file.write('%16.8E%16.8E%16.8E\n' % (0., 0., 0.))
file.close()
