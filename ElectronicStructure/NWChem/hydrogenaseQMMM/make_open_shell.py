#!/usr/bin/env python
#   Script to convert closed shell fmos file to open shell. CHC 08/23/10

import sys
import re

RE1 = re.compile('Number of vector sets is 1')
RE2 = re.compile(' Occupation numbers')
RE3 = re.compile('2.00000')
RE4 = re.compile('Number of vectors in set 1 is')
RE5 = re.compile('SCF energy is \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* Ha')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

occ = False
insert = False

for i in xrange(len(data)-1):
   if RE1.match(data[i]):
      data[i] = re.sub(RE1, 'Number of vector sets is 2', data[i])
   elif RE4.match(data[i]):
      data.insert(i+1, 'Number of vectors in set 2 is' + data[i][-5:])
   elif RE2.match(data[i]):
      occ = True
      insert = True
   elif occ == True:
      if not RE3.search(data[i]):
         occ = False
      else:
         data[i] = re.sub(RE3, '1.00000', data[i])
   if insert == True:
      data.insert(len(data)-2, data[i])

# Add beyond-field-width error handling to this, because Fortran apparently still can't handle errors.
#if RE5.match(data[-2]):
#   data[-2] = re.sub(RE5, 'SCF energy is     0.000000000000 Ha', data[-2])
outfile = open(sys.argv[2], 'w')
for i in data:
   outfile.write(i)
outfile.close()

