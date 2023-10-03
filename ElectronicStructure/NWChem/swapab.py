#!/usr/bin/env python

import re, sys, os

RE1 = re.compile('Occupation')
RE2 = re.compile('SCF')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

if sys.argv[1][-5:] != '.fmos': raise IOError('Input file must have extension .fmos!')
else:
   os.rename(sys.argv[1][0:-5] + '.movecs', sys.argv[1][0:-5]+'a.movecs')
head = []
alpha = []
beta = []
tail = []

counter = 0
for i in data:
   if RE1.search(i) or RE2.search(i):
      counter += 1
   if counter == 0:
      head.append(i)
   elif counter == 1:
      alpha.append(i)
   elif counter == 2:
      beta.append(i)
   elif counter == 3:
      tail.append(i)

outfile = open(sys.argv[1][0:-5] + 'b.fmos', 'w')
for i in head: outfile.write(i)
for i in beta: outfile.write(i)
for i in alpha: outfile.write(i)
for i in tail: outfile.write(i)
outfile.close()
os.remove(sys.argv[1][0:-5] + '.fmos')

