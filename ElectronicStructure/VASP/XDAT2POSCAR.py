#!/usr/bin/env python
# Script to take extract of XDATCAR (no header or tail blanks) and
#   Modify existing POSCAR with new coordinates.
# Scripts sets all atoms to "F", modify mobile atoms by hand.
# CHC 050813

POSCAR_headerlines = 9
numatoms = 51
newgeomfile = open('geom2', 'r')
POSCAR = open('POSCAR', 'r+')

for i in xrange(POSCAR_headerlines):
   POSCAR.readline()
for i in xrange(numatoms):
   t = newgeomfile.readline().strip().split()
   POSCAR.write('%20.16f%20.16f%20.16f%4s%4s%4s\n' % (float(t[0]), float(t[1]), \
            float(t[2]), 'F', 'F', 'F'))
newgeomfile.close()
POSCAR.close()

