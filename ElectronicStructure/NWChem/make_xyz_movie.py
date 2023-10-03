#!/usr/bin/env python
# Script to extract xyz coordinates from NWChem output file
#   to make movie of optimization. CHC 04/20/10

class frame:
   def __init__(self):
      self.atomlist = []
   def add_atom(self, coordinate_string):
      temp = coordinate_string.split()
      element = temp[1]
      x = temp[3]
      y = temp[4]
      z = temp[5]
      self.atomlist.append([element, x, y, z])

import re, sys

RE1 = re.compile('Output coordinates')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

n = int(raw_input('How may atoms in structure?'))

structure_list = []
i = 0
while i < len(data):
   if RE1.search(data[i]):
      i += 4
      new = frame()
      for j in range(i, i + n):
         new.add_atom(data[j])
      i += n
      structure_list.append(new)
   else:
      i += 1

outfile = open(sys.argv[2], 'w')
for i in xrange(len(structure_list)):
   outfile.write(str(n) + '\n')
   outfile.write('Optimization frame ' + str(i) + '\n')
   for j in structure_list[i].atomlist:
      outfile.write(j[0] + '\t' + j[1] + '\t' + j[2] + '\t' + j[3] + '\n')
#   outfile.write('\n')
outfile.close()
