#!/usr/bin/env python
# Script to move atoms in CMTX file along an axis by a user-specified
#   distance (Angstroms) in supercell.

file = open('test.cmtx', 'r')
data = file.readlines()
file.close()

file = open('test2.cmtx', 'w')

axis = 'b'
desired_shift = -0.85

# Amount to scale fractional coordinates by
switch = False  # Required for loop logic below.

axes = {'a':2, 'b':3}
for i in xrange(len(data)):
   if data[i][0:4] == 'CELL':
      t = data[i].split()
      if axis == 'a': fractional_shift = desired_shift / float(t[1])
      elif axis == 'b': fractional_shift = desired_shift / float(t[2])
   if data[i][0:17] == '! Asymmetric unit':
      switch = True
      file.write(data[i] + data[i+1])
      for j in range(i+2,len(data)-1):
         t = data[j].strip().split()
         coor_new = float(t[axes[axis]]) + fractional_shift
         if axis == 'a':
            file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (t[0], t[1], coor_new, \
                       float(t[3]), float(t[4])))
         elif axis == 'b':
            file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (t[0], t[1], float(t[2]), \
                       coor_new, float(t[4])))
   if switch == True:
      file.write('\n')  # Write blank line at end of file
      break
   else:
      file.write(data[i])
file.close()
