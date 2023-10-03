#!/usr/bin/env python
# Script to calculate Weyl dimensions in terms of Slater determinants.
# D_n_Na_Nb: n = number of 2-electron orbitals; Na = number of alpha electrons, etc.

from math import comb

data = {}
n = 5
for a in range(n+1):
   for b in range(n+1):
      Weyl_dim = comb(n,a)*comb(n,b)
      dim_label = 'D_{}_{}_{}'.format(n, a, b)
      print('{} = {}'.format(dim_label, Weyl_dim))
      if Weyl_dim in data: data[Weyl_dim].append(dim_label)
      else: data[Weyl_dim] = [dim_label]
print('Pooled by dimension (account for a/b symmetry)')
print('{:10s}\t{:5s}'.format('Dimension', 'Count'))
total = 0
Pascal_list = []
for i in sorted(data.keys()):
   print('{:10d}\t{:5d}'.format(i, len(data[i])))
   total += len(data[i])
   # For Pascal's triangle like exercise, if counts decrease monotonically
   #    with Dimension (e.g, n=2,4), then no duplication of highest dimension count.
   #    If not monotonic (e.g., n=3), then duplicate.
   Pascal_list.append(i)
print('Total number of determinant occupancies: {}'.format(total))
if n%2 == 0:
   for i in Pascal_list:
      print(i, end=' ')
   Pascal_list.pop(); Pascal_list.reverse()
   for i in Pascal_list:
      print(i, end=' ')
else:
   for i in Pascal_list:
      print(i, end=' ')
   Pascal_list.reverse()
   for i in Pascal_list:
      print(i, end=' ')
print()
