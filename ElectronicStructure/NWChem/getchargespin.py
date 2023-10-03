#!/usr/bin/env python
# Script to take NWChem mulliken output and print atomic charges and spin magnetizations.
#   CHC 2/18/10

import re, sys, gzip

def getdata():
   file.readline()  # Blank line, just skipping
   data = []
   selfflag = True
   while selfflag:
      temp = file.readline().strip().split()
      if len(temp) == 0: selfflag = False  # Blank line ends routine
      if selfflag == False: return data
      atomnum = temp[0]
      element = temp[1]
      charge = float(temp[-1])
      data.append((element, atomnum, charge))
     
RE1 = re.compile('----- Alpha Spin gross population on atoms ----')
RE2 = re.compile('----- Beta Spin  gross population on atoms ----')
element_dict = {'Fe':26., 'S':16., 'O':8., 'N':7., 'C':6., 'H':1.}
if sys.argv[1][-2:] == 'gz':
   file = gzip.open(sys.argv[1], 'r')
else:
   file = open(sys.argv[1], 'r')
flag = True
while flag:
   data = file.readline()
   if RE1.search(data):
      alpha_charges = getdata()
   elif RE2.search(data):
      beta_charges = getdata()
      flag = False
file.close()
print 'Atom\tCharge\tSpinMag'
for i,j in zip(alpha_charges, beta_charges):
   print i[0]+i[1] + '\t' + str(element_dict[i[0]] - i[2] - j[2]) + '\t' + str(i[2] - j[2])
