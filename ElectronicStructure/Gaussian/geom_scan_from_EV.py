#!/usr/bin/env python
# Script to create manual geometry scan structures. Part of 
# project 0651.1101 job FQQ9F8H1XXPVII5t, CHC 12/11

import re
import numpy

class Atom:
   def __init__(self, E, X, Y, Z):
      self.element = E
      self.coords = numpy.array([float(X), float(Y), float(Z)], numpy.float)

RE1 = re.compile(r'%Chk=')
RE2 = re.compile('Title')

EV_scaling_factor = 0.5
Gaussian_template = ['%Chk=', '\n', '#P BLYP/6-311++G(2df,p) DensityFit SCRF(Solvent=n-Octane)\n', '\n', \
'Title', '\n0 1\n']

jobfile = '.gjf'
file = open(jobfile, 'r')
refdata = file.readlines()
file.close()
atomlist = []
for i in refdata[7:25]:
   t = i.strip().split()
   atomlist.append(Atom(t[0], t[1], t[2], t[3]))

refcoords = numpy.zeros((len(atomlist), 3), numpy.float)
for i in xrange(len(atomlist)):
   refcoords[i,:] = atomlist[i].coords

# Get eigenvector
EVarray = EV_scaling_factor * numpy.loadtxt('EV1.txt', usecols=(2,3,4))
for i in xrange(8):
   file = open('scan' + str(i) + '.gjf', 'w')
   #file.write(str(len(atomlist)) + '\n')
   #file.write('Title\n')
   for j in Gaussian_template:
      if RE1.match(j): file.write('%Chk=FQQ9F8_scan' + str(i) + '.chk\n')
      elif RE2.match(j): file.write('Manual scan point ' + str(i) + ' of E008xt product reopt structure along lowest\nfrequency mode in forward reaction direction.\n')
      else: file.write(j)
   newcoords = float(i) * EVarray + refcoords
   for j in xrange(len(atomlist)):
      file.write('%-5s%12.6f%12.6f%12.6f\n' % (atomlist[j].element, newcoords[j,0], newcoords[j,1],newcoords[j,2]))
   file.write('\n')  
   file.close()

# Contents of EV1.txt:
#     1  27     0.03   0.00   0.05
#     2   1     0.16  -0.19  -0.07
#     3   6    -0.04   0.07   0.19
#     4   8    -0.11   0.14   0.28
#     5   6     0.11  -0.03  -0.17
#     6   8     0.19  -0.05  -0.37
#     7   6    -0.01  -0.02   0.08
#     8   8    -0.05  -0.04   0.12
#     9   6     0.13  -0.14   0.01
#    10   1     0.12  -0.15  -0.04
#    11   1     0.19  -0.19   0.12
#    12   6     0.02   0.00   0.06
#    13   1     0.02   0.04   0.14
#    14   6    -0.13   0.04  -0.08
#    15   1    -0.27   0.08   0.01
#    16   1    -0.07   0.01  -0.14
#    17   8    -0.20   0.04  -0.27
#    18   1    -0.27   0.09  -0.17
