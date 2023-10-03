#!/usr/bin/env python
# Script to correct for apparent Crystalmaker bug that forces docked supercell
#   to have gap (too large dim) along a or b.

file = open('slab110.cmtx', 'r')
data = file.readlines()
file.close()

file = open('test.cmtx', 'w')

Crystalmaker_dimension = 12.567
desired_dimension = 11.1720

# Amount to scale fractional coordinates by
scale = Crystalmaker_dimension/desired_dimension
switch = False  # Required for loop logic below.
axis = 'b'

axes = {'a':2, 'b':3}
for i in xrange(len(data)):
   if data[i][0:17] == '! Asymmetric unit':
      switch = True
      file.write(data[i] + data[i+1])
      for j in range(i+2,len(data)-1):
         t = data[j].strip().split()
         coor_new = float(t[axes[axis]]) * scale
         if coor_new > 1.: coor_new -= 1.
         if axis == 'b':
            file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (t[0], t[1], float(t[2]), \
                       coor_new, float(t[4])))
         elif axis == 'a':
            file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (t[0], t[1], coor_new, \
                       float(t[3]), float(t[4])))
   if switch == True:
      file.write('\n')  # Write blank line at end of file
      break
   else:
      file.write(data[i])
file.close()
