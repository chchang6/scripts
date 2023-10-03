#!/usr/bin/env python
# Find all WDES structures in VASP source code from grepped output in file.

import re

RE1 = re.compile('WDES%[A-Z_%]+')

file = open('temp', 'r')
data = file.readlines()
file.close()

things = []
for i in data:
   if RE1.search(i):
      if RE1.search(i).group(0) not in things: things.append(RE1.search(i).group(0))

outfile = open('temp2', 'w')
for i in things: outfile.write(i + '\n')
outfile.close()
