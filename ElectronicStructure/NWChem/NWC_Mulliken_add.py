#!/usr/bin/env python

import re,sys

RE1= re.compile('      Total Density - Mulliken Population Analysis')
RE2= re.compile('      Total Density - Lowdin Population Analysis')

nuclear_charges = {'H':1., 'C':6., 'N':7., 'O':8., 'S':16., 'Fe':26.}

group1 = list(range(197,207)); charge1 = 0.
group2 = list(range(242,252)); charge2 = 0
group3 = list(range(312,332)); charge3 = 0.
group4 = list(range(346,376)); charge4 = 0.

counter = 0

file = open(sys.argv[1], 'r')
while True:
   line = file.readline()
   if line == '': break
   if RE2.match(line):
      counter += 1
      #if counter % 2 != 0: continue
      for i in xrange(4): file.readline()
      for i in xrange(409):
         line = file.readline()
         test = int(line.split()[0])
         if test in group1:
            t = line.split()
            charge1 += nuclear_charges[t[1]] - float(t[3])
         elif test in group2:
            t = line.split()
            charge2 += nuclear_charges[t[1]] - float(t[3])
         elif test in group3:
            t = line.split()
            charge3 += nuclear_charges[t[1]] - float(t[3])
         elif test in group4:
            t = line.split()
            charge4 += nuclear_charges[t[1]] - float(t[3])
      print 'Charge group 1 = %10.6f' % (charge1)
      print 'Charge group 2 = %10.6f' % (charge2)
      print 'Charge group 3 = %10.6f' % (charge3)
      print 'Charge group 4 = %10.6f' % (charge4)
      charge1 = 0.; charge2 = 0.; charge3 = 0.; charge4 = 0.
