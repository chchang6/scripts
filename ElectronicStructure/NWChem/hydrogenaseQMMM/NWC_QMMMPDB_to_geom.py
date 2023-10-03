#!/usr/bin/env python

import sys

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

atoms = []
x = []
y = []
z = []

file = open(sys.argv[2], 'w')
file.write('geometry noautosym noautoz nocenter\n')
for i in data:
   t = i.split()
   file.write('%5s%10.3f%10.3f%10.3f\n' % (t[2], float(t[3]), float(t[4]), float(t[5])))
file.write('end\n')
file.close()
