#!/usr/bin/env python
# Script either to
#  1. displace Cartesian coordinates from Gaussian frequency displacement
#     table from final Berny iteration by either the calculated displacement, or the
#     maximum displacement threshold (0.0018 Bohr), or
#  2. displace Cartesian coordinates by random amount <= 0.01 Bohr.

import sys, math

Bohr_to_Angstrom = 0.52917

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

atoms = ['Co', 'H', 'C', 'O', 'C', 'O', 'C', 'O', 'C', 'H', 'H', 'C', 'H', 'C', 'H', 'H', 'O', 'H']

outfile = open(sys.argv[2], 'w')

for i in xrange(len(data)/3):
   temp = []
   for j in xrange(3):
      x = data[i*3+j].split()
      old = float(x[1])
      disp = float(x[5])
      if math.fabs(disp) > 0.0018:
         temp.append(old + math.copysign(0.0018, disp))
      else:
         temp.append(old + disp)
   outfile.write('%-5s%10.6f%10.6f%10.6f\n' % (atoms[i], temp[0]*Bohr_to_Angstrom, temp[1]*Bohr_to_Angstrom, temp[2]*Bohr_to_Angstrom))
outfile.close()
