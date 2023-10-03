#!/usr/bin/env python3
# Script to take pasted chunk of "Input" or "Standard Orientation" Gaussian
#   output and convert to standard XYZ format for visualization.

import sys

element_dict = { \
   0:'Bq', 1:'H', 6:'C', 7:'N', 8:'O', 9:'F', 14:'Si', 15:'P', 16:'S', 17:'Cl', 25:'Mn', 26:'Fe', 27:'Co', 39:'Y', 44:'Ru', 66:'Dy'}

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

newdata = []
for i in data:
   t = i.strip().split()
   if len(t) > 1:
      newline = '{:2s}      {:10.6f}{:10.6f}{:10.6f}\n'.format(element_dict[int(t[1])], float(t[3]), float(t[4]), float(t[5]))
      newdata.append(newline)

file = open(sys.argv[2], 'w')
file.write(str(len(newdata)) + '\n')
file.write('PBE1PBE/TDZP+ optimized structure of \n')
for i in newdata:
   file.write(i)
file.close()
