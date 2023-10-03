#!/usr/bin/env python
# Script to take XYZ file and create summy Gaussian GJF for input to Gaussview

import sys

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

numatoms = int(data[0].strip())
title = data[1]
if title == '\n': title = 'Title\n'
test_extensions = ['gjf', 'com', 'xyz']
if sys.argv[1][-3:] not in test_extensions:
   file = open(sys.argv[1] + '.gjf', 'w')
else:
   file = open(sys.argv[1][0:-4] + '.gjf', 'w')
file.write('%Mem=0MW\n\n#P B3LYP/6-31G*\n\n' + title + '\n0 1\n')
for i in range(2,numatoms+2):
   file.write(data[i])
file.close()
