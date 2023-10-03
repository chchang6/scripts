#!/usr/bin/env python
# Script to construct sed script to replace CHARMM residue names
#   with AMBER ones. CHC 11/30/09

file = open('built.pdb', 'r')
data = file.readlines()
file.close()

import re

RE1 = re.compile('H[A-Z]+[0-4]')

reslist = []
datalist = []

flag = False
resid = '1'
for i in data:
   x = i.split()
   try:
      if x[5] != resid: flag = False  # We've changed residues; if flag was true, set to false
      resid = x[5]
      if x[3] not in reslist:
         reslist.append(x[3])
         flag = True
      if flag:
         datalist.append(x)
   except IndexError: # Have reached EOF
      continue
   
outfile = open('temp3.sed', 'w')
outfile.write('s/HSD/HID/\n')
for i in datalist:
   if RE1.match(i[2]):
      new_symbol = str(int(i[2][-1])+1) + i[2][0:-1]
      if len(i[2]) == 3:
         sub_string = 's/ ' + i[2] + ' ' + i[3] + '/' + new_symbol + '  ' + i[3] + '/\n'
      elif len(i[2]) == 4:
         sub_string = 's/' + i[2] + ' ' + i[3] + '/' + new_symbol + ' ' + i[3] + '/\n'
      outfile.write(sub_string)
   elif i[2] == 'HN':
      sub_string = 's/HN  ' + i[3] + '/H   ' + i[3] + '/\n'
      outfile.write(sub_string)
outfile.close()

