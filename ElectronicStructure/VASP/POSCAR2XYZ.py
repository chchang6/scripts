#!/usr/bin/env python
# Script to convert POSCAR file to Cartesians.

import numpy
import sys

# Open POSCAR file, which may have a different name.
if len(sys.argv) == 2:
   file = open('POSCAR', 'r')
elif len(sys.argv) == 3:
   file = open(sys.argv[1], 'r')
else:
   sys.exit('Usage: POSCAR2XYZ.py [input file default POSCAR] output_file')
data = file.readlines()
file.close()

# Transformation matrix should be on lines 3-5; element list on line 6;
#   How many of each element on line 7.
row0 = [float(i) for i in data[2].strip().split()]
#print row0
row1 = [float(i) for i in data[3].strip().split()]
#print row1
row2 = [float(i) for i in data[4].strip().split()]
#print row2
elements = data[5].strip().split()
#print elements
numelements = [int(i) for i in data[6].strip().split()]
#print numelements
trans = numpy.asmatrix(numpy.array([row0, row1, row2]))
#print trans

# Coordinates are on lines 10 - 8+numelements[0], etc.
if len(sys.argv) == 2:
   file = open(sys.argv[1], 'w')
elif len(sys.argv) == 3:
   file = open(sys.argv[2], 'w')
else:
   sys.exit('Usage: POSCAR2XYZ.py [input file default POSCAR] output_file')
file.write(str(numpy.sum(numpy.array(numelements))) + '\n')
file.write('Title\n')
counter = 8  # Distance into data. Since counter is incremented to start, this initializes to
#   one less than the first "data" index containing a coordinate line.
for i in xrange(len(numelements)):
   for j in xrange(numelements[i]):
      counter += 1
      frac = numpy.array([float(k) for k in data[counter].strip().split()[0:3]])
      #print numpy.asmatrix(frac).T
      carts = trans * numpy.asmatrix(frac).T
      file.write('%5s%12.6f%12.6f%12.6f\n' % (elements[i], carts[0], carts[1], carts[2]))
file.close()
