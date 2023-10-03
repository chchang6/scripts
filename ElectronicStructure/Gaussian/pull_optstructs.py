#!/usr/bin/env python
# Script to pull optimized XYZ structures from stepwise partial
#   optimization scans.

import sys, re

RE1 = re.compile('Optimization completed')
RE2 = re.compile('Input orientation')
RE3 = re.compile('NAtoms=')

atomdict = {'27':'Co', '1':'H', '6':'C', '8':'O'}

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

# Go through to get number of atoms
for i in data:
   if RE3.search(i):
      t = i.split()
      for j in xrange(len(t)):
         if RE3.match(t[j]): numatoms = int(t[j+1])
      break

outfile = open(sys.argv[2], 'a')

i = 0
while i < len(data):
   t = data[i]
   if RE1.search(data[i]):
      j = 1
      while True:
         t2 = data[i-j]
         if RE2.search(t2):
            outfile.write(str(numatoms) + '\n')
            outfile.write('\n')
            for k in xrange(numatoms):
               t3 = data[i-j+5+k]  # 5 to skip over Input orientation header stuff
               t4 = t3.rstrip().split()
               atom = atomdict[t4[1]]
               x = float(t4[3])
               y = float(t4[4])
               z = float(t4[5])
               outfile.write('%5s%12.6f%12.6f%12.6f\n' % (atom, x, y, z))
            break
         else:
            j += 1
   i += 1
outfile.close()
