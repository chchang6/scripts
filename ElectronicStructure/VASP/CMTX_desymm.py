#!/usr/bin/env python
# Script to generate atoms based on symmetry information in CMTX file

import re

file = open('T1sub.cmtx', 'r')
data = file.readlines()
file.close()

# Clean up some of the data--no atomic error data
i = 0
ERRS = False
while True:
   if ERRS == False:
      try:
         if data[i][0:4] == 'ERRC':
            del(data[i-2:i+1])  # blank, comment, and ERRC line
         elif data[i][0:4] == 'ERRS':
            del(data[i-2:i+1])
            ERRS = True
            i -= 2
            continue
      except IndexError:
         pass
   elif ERRS == True:
      if len(data[i]) < 2:
         break  # End of data
      else:
         del(data[i])
         continue
   i += 1

# Now go through and collect atoms in asymmetric unit
collect = False
elements = []
names = []
indices = []
a = []
b = []
c = []
for i in data:
   if len(i) < 2 and collect == True:
      collect = False
   if i[0:4] == 'ATOM':
      collect = True
   elif collect == True:
      t = i.rstrip().split(None,2)
      a.append(float(i[11:20]))
      b.append(float(i[20:29]))
      c.append(float(i[29:38]))
      elements.append(t[0])
      names.append(re.search('[A-Za-z]+', t[1]).group(0))
      indices.append(int(re.sub('[A-Za-z]', '', t[1])))

# Collect necessary symmetry operations
symmops = []
for i in data:
   if i[0:4] == 'SYMM':
      t = i.strip().split()
      symmop = []
      for j in range(1,4):
         if t[j][0] == '+': symmop.append(1.)
         elif t[j][0] == '-': symmop.append(-1.)
      symmops.append( tuple(symmop) )
symmops.pop(0)  # Redundant identity op

# For each element, for each index, apply symmetry operations and append
#   Assumes elements are contiguous
counter = None
starting_length = len(elements)
for i in xrange(starting_length):
   if counter == None:
      counter = elements.count(elements[i])
   for j in symmops:
      elements.append(elements[i])
      names.append(names[i])
      counter += 1; indices.append(counter)
      a.append(j[0] * a[i])
      b.append(j[1] * b[i])
      c.append(j[2] * c[i])
   counter = None

# Now create new lists with sorted atom orders
new_elements = []
new_names = []
new_indices = []
new_a = []
new_b = []
new_c = []
for i in set(elements):
   for j in xrange(len(elements)):
      if elements[j] == i:
         new_elements.append(elements[j])
         new_names.append(names[j])
         new_indices.append(indices[j])
         new_a.append(a[j])
         new_b.append(b[j])
         new_c.append(c[j])

# Dump out coordinates that can be dropped into a CMTX file from Crystalmaker
file = open('test.frac', 'w')
for i in xrange(len(new_elements)):
   file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (new_elements[i], new_names[i]+str(new_indices[i]), \
     new_a[i], new_b[i], new_c[i]))
file.close()
