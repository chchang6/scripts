#!/usr/bin/env python
# Script either to
#  Displace Cartesian coordinates from Gaussian frequency displacement
#  table from final Berny iteration by either the calculated displacement, or the
#  maximum displacement threshold (0.0018 Bohr), or

import sys, math
import re
from random import uniform

RE1 = re.compile('Standard orientation')
RE2 = re.compile('-------')
RE_maxdisp = re.compile(' Maximum Displacement')

Bohr_to_Angstrom = 0.52917
element_dict = { \
   0:'Bq', 1:'H', 6:'C', 7:'N', 8:'O', 9:'F', 14:'Si', 16:'S', 17:'Cl', 25:'Mn', 26:'Fe', 27:'Co', 44:'Ru'}

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

in_logfile_iterator = iter(data)
max_displacement = None

while True:
   try:
      test_line = next(in_logfile_iterator)
      if RE1.search(test_line):
         for i in range(4): next(in_logfile_iterator)
         geom = []
         while True:
            t2 = next(in_logfile_iterator).split()
            if RE2.match(t2[0]): break
            el = element_dict[int(t2[1])]
            coords = [float(t2[i]) for i in range(3,6)]
            geom.append( (el, coords) )
      elif RE_maxdisp.match(test_line):
         max_displacement = min(float(test_line.split()[2]), 0.0018)
   except StopIteration:
      break
# Have reached end of iterator on data, so geom carries last geometry of optimization.

outfile = open(sys.argv[2], 'w')
for i in geom:
   new_x = i[1][0] + uniform(-1.*max_displacement/Bohr_to_Angstrom, max_displacement/Bohr_to_Angstrom)
   new_y = i[1][1] + uniform(-1.*max_displacement/Bohr_to_Angstrom, max_displacement/Bohr_to_Angstrom)
   new_z = i[1][2] + uniform(-1.*max_displacement/Bohr_to_Angstrom, max_displacement/Bohr_to_Angstrom)
   outfile.write("{:<5s}{:10.6f}{:10.6f}{:10.6f}\n".format(i[0], new_x, new_y, new_z))
outfile.close()
