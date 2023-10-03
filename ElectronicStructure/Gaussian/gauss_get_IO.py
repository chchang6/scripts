#!/usr/bin/python
# Script to extract input orientation geometries of a Gaussian optimization
# and write them out in XYZ format.
# gauss_get_IO.py X.log

import re, sys

RE1 = re.compile('Input orientation')
RE2 = re.compile(' ---------')

numatoms = 0
elements = {'1':'H', '6':'C', '7':'N', '8':'O', '16':'S', '26':'Fe', \
'27':'Co'}

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

# Get number of atoms
i = 0
while True:
   if RE1.search(data[i]):
      i += 5
      while True:
         if RE2.match(data[i]):
            break
         else:
            i += 1
            numatoms += 1
      break
   else: i += 1
   
# Accumulate structures
outdata = []
for x in xrange(len(data)):
   if RE1.search(data[x]):
      outdata.append(str(numatoms))
      outdata.append('\n\n')
      for y in xrange(numatoms):
         rawdata = data[x+y+5].split()
         outstring = elements[rawdata[1]] + '   ' + rawdata[3] + '   ' + rawdata[4] + '   ' + rawdata[5] + '\n'
         outdata.append(outstring)

# Delete last structure, which is just a report of the n-1th one.
outdata = outdata[0:-1*(numatoms+2)]

# Write out to file
outfile = open('trajectory.xyz', 'w')
for i in outdata:
   outfile.write(i)
outfile.close()
