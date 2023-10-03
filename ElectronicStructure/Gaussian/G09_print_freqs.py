#!/usr/bin/env python
# Script to extract normal mode info and print frequencies
#    ordered by magnitude of particular atom's contribution

import re

job = 'F9dIwK4jWH'
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
have_geometry = False

name_dict = {'1':'H', '6':'C', '7':'N', '8':'O', '16':'S', '26':'Fe'}

file = open(job + '.log', 'r')
while True:
   data = file.readline()
   if RE2.match(data) and have_numatoms == False:
      #print 'RE2 matches'
      numatoms = int(data.split()[1])
      have_numatoms = True
   elif RE3.search(data) and have_geometry == False:
      if numatoms == 0: continue
      #print 'RE3 matches'
      for i in xrange(4): file.readline()
      for i in xrange(numatoms):
         t = file.readline().strip().split()
         names.append(name_dict[t[1]])
         coordinates.extend(t[3:6])
      have_geometry = True
   elif RE1.match(data):
      for i in xrange((3*numatoms - 6)/3):
         data1 = file.readline().rstrip()
         mode_index = data1[17:].split()
         mode_numbers.extend([int(j) for j in mode_index])
         for j in xrange(len(mode_index)):
            modes[mode_numbers[-1] - j] = []
         file.readline()
         freq_data = file.readline().rstrip()
         freq_data = freq_data[17:].split()
         frequencies.extend([float(j) for j in freq_data])
         RM_data = file.readline().rstrip()
         RM_data = RM_data[17:].split()
         reduced_masses.extend([float(j) for j in RM_data])
         for j in xrange(3): file.readline()
         for j in xrange(numatoms):
            t = file.readline().strip().split()
            for k in xrange(len(mode_index)):
               modes[mode_numbers[-1] - len(mode_index) + 1 + k].extend([float(l) for l in t[2 + 3*k : 2 + 3*k + 3] ])
   if len(modes) > 0: break

user_atom = raw_input('Enter a particular atom index (1-based) of interest (return for unsorted) ')
if user_atom != '':
   user_index = int(user_atom)
   mode_components = []
   for i in xrange(len(modes)):
      mode_components.append(modes[i+1][user_index-1])
   sorted_modes = []
   not_visited = list( xrange(len(mode_components)) )
   visited = []
   temp = 0
   while len(not_visited) > 0:
      ref = 0.
      refindex = -1
      for j in not_visited:
         if abs(mode_components[j]) >= ref:  # Doesn't matter what order if mode values are equal.
            signed = mode_components[j]
            ref = abs(mode_components[j])
            refindex = j
      sorted_modes.append( (refindex+1, signed) )   # Print out 1-indexed for mode #
      visited.append(refindex)
      not_visited.remove(refindex)
   for i in sorted_modes:
      print 'Mode %3i Reduced mass %8.3f Frequency %8.3f Component %5s' % \
         (i[0], reduced_masses[i[0]-1], frequencies[i[0]-1], i[1])
else:
   for i in xrange(len(modes)):
      print 'Mode %3i Reduced mass %8.3f Frequency %8.3f' % (i+1, reduced_masses[i], frequencies[i])
