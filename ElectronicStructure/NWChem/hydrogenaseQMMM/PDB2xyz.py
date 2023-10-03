#!/usr/bin/env python
import sys
file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()
outfile = open('active.xyz', 'w')
for i in data:
   temp = i.strip().split()
   outfile.write(temp[2] + '   ' + temp[3] + '   ' + temp[4] + '   ' + temp[5] + '\n')
outfile.close()
