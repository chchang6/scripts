#!/usr/bin/env python
# Script to create XYZ movie file from concatenated XDATCAR and OUTCAR files.
# Require files "XDATCAR" and "OUTCAR". If there are multiple restarts, create these by
#   cat XDATCAR.1 XDATCAR.2 ... > XDATCAR
# and similar for OUTCAR.
# Example usage "./catXDAT.py movie.xyz"

import sys, re
import numpy
from os.path import exists as file_exists

RE1 = re.compile('F=')  # RE to parse OSZICAR
RE2 = re.compile('free  energy')  # RE to parse OUTCAR

# Get unit cell and elemental data from CONTCAR
file = open('CONTCAR', 'r')
unit = []
for i in xrange(7):
   x = file.readline()
   if i == 2 or i == 3 or i == 4:
      unit.append(x)
   elif i == 5:
      elements = x.strip().split()
   elif i == 6:
      temp = x.strip().split()
      atomnums = []
      numatoms = 0
      for j in temp:
         atomnums.append(int(j))
         numatoms += int(j)
file.close()
print 'Done with file CONTCAR'
#DEBUG
#print unit
#print elements
#print atomnums
#print numatoms

# Create dumb list of atom types for later
atomtypes = []
for i in xrange(len(atomnums)):
   for j in xrange(atomnums[i]):
      atomtypes.append(elements[i])
# DEBUG
#print atomtypes

# Make transformation array from unit cell data.
unitcell = numpy.zeros((3,3), numpy.float)
for i in xrange(3):
   x = unit[i].split()
   for j in xrange(3):
      unitcell[i,j] = float(x[j])
#DEBUG
#print unitcell

# XDATCAR may be a concatenation of multiple runs, so we need to renumber the Konfigs consecutively.
file = open('XDATCAR', 'r')
data = file.readlines()
file.close()
print 'Done reading file XDATCAR'
counter = 1
for i in xrange(len(data)):
   if data[i][0:7] == ' Konfig':
      x = data[i].split()
      data[i] = ' Konfig=%12i\n' % counter
      counter += 1
   elif data[i][0:20] == 'Direct configuration':
      x = data[i].split()
      data[i] = 'Direct configuration=%12i\n' % counter
      counter += 1
print 'There are ' + str(counter) + ' structures in this optimization'

# Grab each ionic energy from OSZICAR (preferably), or OUTCAR (assume one is available).
energies = []
energy_file = None
if file_exists('./OSZICAR'):
   file = open('OSZICAR', 'r')
   energy_file = 'OSZICAR'
elif file_exists('./OUTCAR'):
   file = open('OUTCAR', 'r')
   energy_file = 'OUTCAR'
else:
   sys.exit('Script requires either OSZICAR or OUTCAR')
i = 0
while i < counter-1:
   x = file.readline()
   if energy_file == 'OSZICAR' and RE1.search(x):
      t = float(x[7:22])
      energies.append('%10.4f' % t)
      i += 1
      if i%100 == 0:
         print 'Done getting ' + str(i) + 'th energy'
   elif energy_file == 'OUTCAR' and RE2.search(x):
      energies.append(x.rstrip()[-20:])
      i += 1
      if i%100 == 0:
         print 'Done getting ' + str(i) + 'th energy'
file.close()
print 'Done with energy file'

# Transform coordinates
for i in xrange(len(data)):
   if data[i][0:7] == ' Konfig' or data[i][0:20] == 'Direct configuration':
      temp = data[i+1:i+1+numatoms]
      for j in xrange(len(temp)):
         x = numpy.array(temp[j].strip().split(), numpy.float)
         frac = numpy.reshape(x, (3,1))
         cart = numpy.asmatrix(unitcell) * numpy.asmatrix(frac)
         cart = numpy.reshape(numpy.asarray(cart), (1,3))
         data[i+j+1] = '%13.8f%13.8f%13.8f\n' % (cart[0][0], cart[0][1], cart[0][2])
      
outfile = open(sys.argv[1], 'w')
counter = 0
strnumatoms = str(numatoms) + '\n'
for i in xrange(len(data)):
   if data[i][0:7] == ' Konfig' or data[i][0:20] == 'Direct configuration':
      outfile.write(strnumatoms)
      outfile.write('Frame ' + str(counter+1) + ' Energy ' + energies[counter] + '\n')
      for j in xrange(numatoms):
         outfile.write(atomtypes[j] + '   ' + data[i+j+1])
      counter += 1
outfile.close()
