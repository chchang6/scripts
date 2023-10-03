#!/usr/bin/env python
# Script to convert Crystalmaker CMTX file to VASP POSCAR file
# CHC 022613
# CHC 032213 Modify to handle FCC cell output from Crystalmaker
# CHC 042613 Modify to handle multiple CMTX files automatically read from directory. New script CMTX2POSCAR2
# CHC 042913 Modify to automatically make ligand-only POSCAR files.

import os, fnmatch, copy
import re, math
import numpy
import sys

RE1 = re.compile('CELL')
RE2 = re.compile('ATOM')
RE3 = re.compile('LATC')

# User data
# If surface material shares elements with ligands, this script will fail to autogenerate ligand-only files.
surface_elements = ['Pd']

CMTX_files = []

try:
   CMTX_files.append(sys.argv[1])
except IndexError:
   for i in os.listdir('.'):
      if fnmatch.fnmatch(i, 'Pd100_*.cmtx'): CMTX_files.append(i)

for i in CMTX_files:
   basename = i.rstrip('.cmtx')
   t = basename.split('_')
   ligand = t[1]
   feature = t[2]
   VASP_title = 'Pd 100 slab plus ' + ligand + ' bound to ' + feature
   # Need to build ligand alone only once. Choose the "top" feature arbitrarily.
   if feature == 'top':
      VASP_ligand_title = 'Ligand ' + ligand
   file = open(i, 'r')
   data = file.readlines()
   file.close()

   # Get relevant information from input data.
   for j in data:
      if RE3.match(j):
         t = j.rstrip().split()
         if t[1] == 'F': face_centered = True
      elif RE1.match(j):
         t = j.strip().split()
         [a,b,c] = [float(k) for k in t[1:4]]
         [alpha,beta,gamma] = [math.radians(float(k)) for k in t[4:]]
      elif RE2.match(j):
         atoms = []
         fracs = []
         # Keep track of ligand atoms in all systems so constraints can be set below
         ligatoms = []
         ligfracs = []
         refline = data.index(j)
         k = 1
         while True:
            if data[refline + k] == '\n': break
            else:
               temp = data[refline + k].split()
               atoms.append(temp[0])
               fracs.append([float(l) for l in temp[2:5]])
               if temp[0] not in surface_elements:
                  ligatoms.append(temp[0])
                  ligfracs.append([float(l) for l in temp[2:5]])
               k += 1
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
   ligand_atomtypes = []
   for j in atoms:
      if j not in atomtypes: atomtypes.append(j)
   if feature == 'top':
      for j in ligatoms:
         if j not in ligand_atomtypes: ligand_atomtypes.append(j)
   atomcounts = [ atoms.count(j) for j in atomtypes ]
   if feature == 'top':
      ligand_atomcounts = [ atoms.count(j) for j in ligand_atomtypes ]
   
   # Write out output data
   file = open('POSCAR_' + ligand + '_' + feature, 'w')
   file.write(VASP_title + '\n')
   file.write('%19.14f\n' % (1.0))
   file.write('  %21.16f%21.16f%21.16f\n' % (a_cart[0,0], a_cart[1,0], a_cart[2,0]) )
   file.write('  %21.16f%21.16f%21.16f\n' % (b_cart[0,0], b_cart[1,0], b_cart[2,0]) )
   file.write('  %21.16f%21.16f%21.16f\n' % (c_cart[0,0], c_cart[1,0], c_cart[2,0]) )
   for j in atomtypes:
      file.write('   %-2s' % (j))
   file.write('\n')
   for j in atomcounts:
      file.write('%4i' % (j))
   file.write('\n')
   file.write('Selective dynamics\n')
   file.write('Direct\n')
   for j in xrange(len(fracs)):
      if j < len(ligfracs):
         # Make ligand atoms mobile for optimization
         file.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (fracs[j][0], fracs[j][1], fracs[j][2], 'T', 'T', 'T'))
      else:
         file.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (fracs[j][0], fracs[j][1], fracs[j][2], 'F', 'F', 'F'))
   file.write('\n')
   for j in xrange(len(fracs)):
      file.write('%16.8E%16.8E%16.8E\n' % (0., 0., 0.))
   file.close()

   if feature == 'top':
      ligand_file = open('POSCAR_' + ligand, 'w')
      ligand_file.write(VASP_ligand_title + '\n')
      ligand_file.write('%19.14f\n' % (1.0))
      ligand_file.write('  %21.16f%21.16f%21.16f\n' % (a_cart[0,0], a_cart[1,0], a_cart[2,0]) )
      ligand_file.write('  %21.16f%21.16f%21.16f\n' % (b_cart[0,0], b_cart[1,0], b_cart[2,0]) )
      ligand_file.write('  %21.16f%21.16f%21.16f\n' % (c_cart[0,0], c_cart[1,0], c_cart[2,0]) )
      for j in ligand_atomtypes:
         ligand_file.write('   %-2s' % (j))
      ligand_file.write('\n')
      for j in ligand_atomcounts:
         ligand_file.write('%4i' % (j))
      ligand_file.write('\n')
      ligand_file.write('Selective dynamics\n')
      ligand_file.write('Direct\n')
      for j in ligfracs:
         ligand_file.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (j[0], j[1], j[2], 'T', 'T', 'T'))
      ligand_file.write('\n')
      for j in xrange(len(ligfracs)):
         ligand_file.write('%16.8E%16.8E%16.8E\n' % (0., 0., 0.))
      ligand_file.close()
