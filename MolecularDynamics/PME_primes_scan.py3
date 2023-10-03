#!/usr/bin/env python
# Molecular dynamics Particle Mesh Ewald works best when grids are dimensioned
#   as products of small prime numbers. This script just steps through low powers
#   of 2, 3, and 5 and prints products thereof. Commas are placed for intended
#   downstream parsing as CSV.

for i in range(1,25):
   print("(2^{0}) , , = ,{1}".format(i, 2**i))
for i in range(1,16):
   print(" , (3^{0}), = ,{1}".format(i, 3**i))
for i in range(1,11):
   print(" , , (5^{0}) = ,{1}".format(i, 5**i))

for i in range(1,11):
   for j in range(1,11):
      print("(2^{0}) * ,(3^{1}), = ,{2}".format(i, j, 2**i * 3**j))
for i in range(1,11):
   for j in range(1,11):
      print("(2^{0}) *, , (5^{1}) = ,{2}".format(i, j, 2**i * 5**j))
for i in range(1,11):
   for j in range(1,11):
      print(" , (3^{0}) *, (5^{1}) = ,{2}".format(i, j, 3**i * 5**j))

for i in range(1,11):
   for j in range(1,11):
      for k in range(1,11):
         print("(2^{0}) *, (3^{1}) *, (5^{2}) = ,{3}".format(i, j, k, 2**i * 3**j * 5**k))
