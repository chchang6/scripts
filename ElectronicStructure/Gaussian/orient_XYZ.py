#!/usr/bin/env python
# Script to read in XYZ trajectory file and orient structures
#   with selected bond along +x axis. CHC 102313

import sys
import math
import numpy

def rotate_y(coors, angle):
   rotation_matrix = numpy.matrix([ \
    [ math.cos(angle), 0.0, -math.sin(angle)], \
    [ 0.0, 1.0, 0.0 ], \
    [ math.sin(angle), 0.0, math.cos(angle) ]])
   #print 'rotate_y: coors shape is ' + str(numpy.shape(coors))
   return (rotation_matrix * coors.T).T

def rotate_z(coors, angle):
   rotation_matrix = numpy.matrix([ \
    [ math.cos(angle), math.sin(angle), 0.0], \
    [ -math.sin(angle), math.cos(angle), 0.0], \
    [ 0.0, 0.0, 1.0 ]])
   #print 'rotate_z: coors shape is ' + str(numpy.shape(coors))
   #print 'rotate_z: rotation_array shape is ' + str(numpy.shape(rotation_matrix))
   return (rotation_matrix * coors.T).T

atom1 = 76   # 1-indexed atom index to place at origin
atom2 = 78   # 1-indexed atom index to place on +x
file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

numatoms = int(data[0].strip())
titles = []
for i in range(1, len(data), numatoms+2):
   titles.append(data[i])

elements = []
outfile = open(sys.argv[1][0:-4] + '_rot.xyz', 'w')
for i in range(2, len(data), numatoms+2):
   structure = []
   for j in xrange(numatoms):
      structure.append([ float(k) for k in data[i+j].strip().split()[1:]])
      if i == 2:
         elements.append(data[i+j].strip().split()[0])
   structure = numpy.matrix(structure)
   # Translate to atom1
   t = structure - structure[atom1-1,:]
   # Rotate around z so atom2 in xz plane
   angle = math.atan2(t[atom2-1,1], t[atom2-1,0])
   t = rotate_z(t, angle)
   # Rotate around y so atom2 on x
   angle = -1.*math.atan2(t[atom2-1,2], t[atom2-1,0])
   t = rotate_y(t, angle)
   outfile.write(str(numatoms) + '\n')
   outfile.write(titles[(i-2)/(numatoms+2)])
   for j in xrange(len(elements)):
      outfile.write('%-5s%10.6f%10.6f%10.6f\n' % (elements[j], t[j,0], t[j,1], t[j,2]))
outfile.close()
