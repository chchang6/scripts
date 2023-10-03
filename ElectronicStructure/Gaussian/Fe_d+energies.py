#!/usr/bin/env python

import re

RE1 = re.compile('NBO 5\.9')
RE2 = re.compile('  NAO')
RE3 = re.compile('SCF Done')
RE4a = re.compile(' Alpha  occ\.')
RE4b = re.compile(' Alpha virt\.')
RE5a = re.compile('  Beta  occ\.')
RE5b = re.compile('  Beta virt\.')
RE6 = re.compile(' S\*\*2')

Feprox = '1'  # atom index of proximal Fe (1-indexed)
Fedist = '2'  # atom index of distal Fe (1-indexed)
Feproxdpop = 0.0
Fedistdpop = 0.0
delta = 1e-6

logfile = ''
file = open(logfile, 'r')
data = file.readlines()
file.close()
data.reverse()
for i in xrange(len(data)):
   if RE1.search(data[i]):
      for j in xrange(1000):
         t = data[i-j].split()
         if len(t) < 3: continue
         if t[1] == 'Fe' and t[2] == Fedist and t[3][0] == 'd':
            Fedistdpop += float(t[-2])
         elif t[1] == 'Fe' and t[2] == Feprox and t[3][0] == 'd':
            Feproxdpop += float(t[-2])
         elif abs(Feproxdpop-0.0) > delta and (Fedistdpop-0.0) > delta and t[1] != 'Fe':
            break
      break
print 'Proximal Fe d occupancy is %8.5f' % (Feproxdpop)
print 'Distal Fe d occupancy is %8.5f' % (Fedistdpop)

# Get total energy and HOMO LUMO energies
for i in xrange(len(data)):
   if RE3.search(data[i]):
      t = data[i].split('=')
      print 'Total TZVP+ energy = ' + t[1].split()[0]
      break
   elif RE6.match(data[i]):
      t = data[i].rstrip().split()
      print 'S**2 = ' + t[-1]
   elif RE5b.match(data[i]) and RE5a.match(data[i+1]):
      bHOMO = float(data[i+1].split()[-1])
      bLUMO = float(data[i].split()[4])
   elif RE4b.match(data[i]) and RE4a.match(data[i+1]):
      aHOMO = float(data[i+1].split()[-1])
      aLUMO = float(data[i].split()[4])
print 'alpha HOMO energy = %10.5f Ha\nalpha LUMO energy = %10.5f Ha' % (aHOMO, aLUMO)
print 'beta HOMO energy = %10.5f Ha\nbeta LUMO energy = %10.5f Ha' % (bHOMO, bLUMO)

