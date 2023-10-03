#!/usr/bin/env python
# Script to extract normal mode info for visualization in VMD
#   using nmwiz plugin.

import re

job = '3zLbrLNu8q2e'
RE1 = re.compile(' and normal coordinates')
RE2 = re.compile(' NAtoms=')
RE3 = re.compile('Standard orientation:')

numatoms = 0 # Dummy value, set later
names = []
coordinates = []
mode_numbers = []
frequencies = []
reduced_masses = []
modes = {}
have_numatoms = False

name_dict = {'1':'H', '6':'C', '7':'N', '8':'O', '16':'S', '26':'Fe'}

file = open(job + '.log', 'r')
data = file.readlines()
file.close()

# First get number of atoms
for i in data:
   if RE2.match(i) and have_numatoms == False:
      numatoms = int(i.split()[1])
      have_numatoms = True
      break

# Next, get standard orientation geometry
for i in range(len(data)-1, 1, -1):
   if RE3.search(data[i]):
      for j in xrange(i+5, i+5+numatoms):
         t = data[j].strip().split()
         names.append(name_dict[t[1]])
         coordinates.extend(t[3:6])
      break

# Now get modes
for i in xrange(len(data)):
   if RE1.match(data[i]):
      for j in xrange((3*numatoms - 6)/3):
         data1 = data[i+j*(numatoms+7)+1].rstrip()
         mode_index = data1[17:].split()
         mode_numbers.extend([int(k) for k in mode_index])
         for k in xrange(len(mode_index)):
            modes[mode_numbers[-1] - k] = []
         freq_data = data[i+j*(numatoms+7)+3].rstrip()
         freq_data = freq_data[17:].split()
         frequencies.extend([float(k) for k in freq_data])
         RM_data = data[i+j*(numatoms+7)+4].rstrip()
         RM_data = RM_data[17:].split()
         reduced_masses.extend([float(k) for k in RM_data])
         for k in range(8,numatoms+8):
            t = data[i+j*(numatoms+7)+k].strip().split()
            for l in xrange(len(mode_index)):
               modes[mode_numbers[-1] - len(mode_index) + 1 + l].extend([float(m) for m in t[2 + 3*l : 2 + 3*l + 3] ])
   if len(modes) > 0: break

for i in xrange(len(modes)):
   print 'Mode %3i Reduced mass %8.3f Frequency %8.3f' % (i+1, reduced_masses[i], frequencies[i])
outfile = open(job + '.nmd', 'w')
outfile.write('title ' + job + '\n')
outfile.write('names ')
for i in names:
   outfile.write('%3s' % (i))
outfile.write('\n')
outfile.write('coordinates ')
for i in coordinates:
   outfile.write('%12s' % (i))
outfile.write('\n')
for i in xrange(len(modes)):
   outfile.write('mode %3i %5.2f' % (i+1, 1.0))
   #outfile.write('mode %3i %5.2f' % (i+1, reduced_masses[i]))
   for j in modes[i+1]:
      outfile.write('%7.3f' % j)
   outfile.write('\n')
outfile.close()
