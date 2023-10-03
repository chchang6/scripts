#!/usr/bin/env python
# Script to fix bogus scaling in scale.py after fixing Crystalmaker gaps.

file = open('test.cmtx', 'r')
data = file.readlines()
file.close()

file = open('test2.cmtx', 'w')

a_length_actual = 3.023  # Distance between adjacent atoms along a
b_length_actual = 5.238  # Distance between adjacent atoms along b
a_length_desired = 2.793  # Distance between adjacent atoms along a
b_length_desired = 2.793  # Distance between adjacent atoms along b

# Just need to compress unit cell dimensions by appropriate amount
scale_a = a_length_desired/a_length_actual
scale_b = b_length_desired/b_length_actual
for i in xrange(len(data)):
   if data[i][0:4] == 'CELL':
      t = data[i].split()
      a_actual = float(t[1]); a_new = a_actual * scale_a
      b_actual = float(t[2]); b_new = b_actual * scale_b
      #CELL  12.092560 20.944929 15.000000  135.000000 90.000000 60.000000
      data[i] = 'CELL %.6f %.6f %.6f  %.6f %.6f %.6f\n' % \
      (a_new, b_new, float(t[3]), float(t[4]), float(t[5]), float(t[6]))
   file.write(data[i])
file.close()
