#!/usr/bin/env python
#   Script to extract Cartesians for intermediate geometries from optimization
#   output.

import re, sys

RE1 = re.compile('Geometry \"')
RE2 = re.compile('No\. of atoms')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

numatoms = 0
for i in data:
   if RE2.search(i) and numatoms == 0:
      numatoms = int(i.strip().split(':')[1])
      break

outfile = open(sys.argv[2], 'w')

for i in xrange(len(data)):
   x = data[i]
   if RE1.search(x):
      temp = data[i+7:i+7+numatoms]
      outfile.write(str(numatoms) + '\n')
      outfile.write('\n')
      for j in temp:
         x = j.strip().split()
         outfile.write('%5s%15.8f%15.8f%15.8f\n' % (x[1], float(x[3]), float(x[4]), float(x[5])))
outfile.close()
