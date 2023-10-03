#!/usr/bin/env python
#   Script to parse NWChem TDDFT data
#   CHC 11/10/10

import sys, re

class datum:
   def __init__(self, r, m, s, e):
      self.rootnum = int(r)
      if m == 'singlet':
         self.mult = 1
      elif m == 'triplet':
         self.mult = 3
      else:
         sys.exit('Can\'t parse root multiplicity: ' + m)
      self.sym = s
      self.energy = float(e)  # Transition energy in eV
      self.moment = None  # (X, Y, Z)
      self.OS = None  # Oscillator strength
      self.complist = []  # List of orbital pairs, coefficients, and XYZ

class component:
   def __init__(self, dn, ds, an, as, cf, a):
      self.donornum = int(dn)
      self.donorsym = ds
      self.accnum = int(an)
      self.accsym = as
      self.coeff = float(cf)
      self.XYZ = a

def parse(line_number, number_of_roots):
   l = []
   # Start parsing at first Root line of a group of roots.
   counter = line_number
   for i in xrange(number_of_roots):
      x1 = data[counter].split()
      x2 = datum(x1[1], x1[2], x1[3], x1[7])
      counter += 2
      x3 = data[counter].split()
      if x3[-1] == 'forbidden':
         x2.moment = (0., 0., 0.)
         x2.OS = 0.0
         counter += 2
      else:
         x2.moment = (float(x3[3]), float(x3[5]), float(x3[7]))
         counter += 1
         x4 = data[counter].strip().split()
         x2.OS = float(x4[-1])
         counter += 1
      test = True
      while test:
         counter += 1
         if RE2.match(data[counter].strip()):
            counter += 1
            test = False
         elif RE4.match(data[counter]):
            test = False
         else:
            x5 = data[counter].strip().split()
            x2.complist.append(component(x5[1], x5[2], x5[5], x5[6], x5[7], x5[8]))
      l.append(x2)
   return l, counter

RE1 = re.compile('Root')
RE2 = re.compile('---------------')
RE3 = re.compile('No\. of roots')
RE4 = re.compile(' \n')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()
outfile = open(sys.argv[2], 'w')

# There may be only singlets, only triplets, or both in output file.
#  Prompt user.
#st = raw.input('Should I parse just singlets(S), just triplets(T), or both(ST)? ')
i = 0
while i < len(data):
   temp = data[i].strip()
   if RE3.match(temp):
      x = temp.split(':')
      numroots = int(x[1].lstrip())
   elif RE1.match(temp):  # Begin first section of data. Call parser.
      y, i = parse(i, numroots)
      if y[0].mult == 1:
         outfile.write('Singlet manifold\n')
      elif y[0].mult == 3:
         outfile.write('Triplet manifold\n')
      else:
         outfile.close()
         sys.exit('Don\'t know what mutiplicity ' + str(y[0].mult) + ' is!')
      outfile.write('Transition\tSymmetry\tEnergy(eV)\tTransition Moment\t\t\tOsc Strength\tComposition\n')
      outfile.write('\t\t\tX\tY\tZ\t\t\n')
      for j in y:
         outfile.write(str(j.rootnum) + '\t')
         outfile.write(j.sym + '\t')
         outfile.write(str(j.energy) + '\t')
         for k in [0, 1, 2]:
            outfile.write(str(j.moment[k]) + '\t')
         outfile.write(str(j.OS) + '\t')
         for k in xrange(len(j.complist)):
           # if k != 0:
           #    outfile.write('\t\t\t\t\t\t\t')
            outfile.write(str(j.complist[k].donornum) + '(' + \
             j.complist[k].donorsym + ') --> ' + \
             str(j.complist[k].accnum) + '(' + \
             j.complist[k].accsym + ') ' + str(j.complist[k].coeff) + \
             j.complist[k].XYZ + 'break')
         outfile.write('\n')
   i += 1
outfile.close()
