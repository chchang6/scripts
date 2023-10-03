#!/usr/bin/env python
# Take as input either just number of ranks per node,
#   or that and a number of cores that each rank should be pinned
#   to (usually 1). Then dump out string suitable for Slurm's
#   --cpu-bind option on Eagle

import sys

cores_per_node = 36 # Fix for now

if len(sys.argv) > 1:
   try:
      ranks_per_node = int(sys.argv[1])
   except TypeError:
      sys.exit('First argument must be integer ranks per node')
else:
   sys.exit('You must provide ranks/node as a mandatory argument')   

cores_per_rank = cores_per_node // ranks_per_node # Default value

if len(sys.argv) > 2:
   try:
      cores_per_rank = int(sys.argv[2])
   except TypeError:
      sys.exit('Optional second argument must be integer cores per rank')

# If there are fewer cores_per_rank than the default, want stride below
#    to be wider
if cores_per_rank < cores_per_node // ranks_per_node:
   stride = cores_per_node // ranks_per_node
else:
   stride = cores_per_rank

assert ranks_per_node < cores_per_node, "No oversubscription!"

map_strings = []
mapdict = dict(zip(list(range(ranks_per_node)), [None for i in range(ranks_per_node)]))

for i in mapdict:
   t = []
   for j in range(cores_per_rank):
      t.append(i*stride + j)
   mapdict[i] = t

#print(mapdict)

# Look for ranks split over 2 sockets (i.e., that have value list with a number < 18 and a number > 17)
# Assume user should plan this correctly, and if they don't, job will bomb.
len_hex_string = cores_per_node // 4 + 2 # Each hex number codes 4 binary digits. Add 2 for 0x
for i in mapdict:
   if not (all(j < 18 for j in mapdict[i]) or all(j > 17 for j in mapdict[i])):
      sys.exit('Rank %d is split over sockets' % (i))
   else: # Convert value list to hex mask
      mask = ['0' for j in range(cores_per_node)]
      for j in mapdict[i]:
         mask[(cores_per_node - 1) - j] = '1'
      mapdict[i] = "{0:#0{1}x}".format(int(''.join(mask), 2), len_hex_string)

#print(mapdict)

# Now dump in Slurm-friendly format
t = ''
for i in sorted(mapdict.keys()):
   t += mapdict[i] + ','
print(t[:-1])

