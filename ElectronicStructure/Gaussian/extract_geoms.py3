#!/usr/bin/env python3

import re, sys, os
from os.path import exists
from shutil import copyfile

RE3 = re.compile('Step')
RE4a = re.compile('Q-Chem')
RE4b = re.compile(' Entering Gaussian System')

def qchem(itater):
   global prior_file
   RE1 = re.compile('Standard Nuclear Orientation \(Angstroms\)')
   RE2 = re.compile(' --------')
   numatoms = 0; numgeoms = 0
   outdata = []
   for x in itater:
      if RE1.search(x):
         if prior_file:
            prior_file = False
            continue
         numgeoms += 1
         next(itater); next(itater)
         while True:
            t = next(itater)
            if RE2.match(t):
               break
            else:
               if numgeoms == 1: numatoms += 1
               rawdata = t.split()
               outstring = '{}   {}  {}  {}'.format(rawdata[1], rawdata[2], rawdata[3], rawdata[4])
               outdata.append(outstring)
   return numatoms, numgeoms, outdata

def gaussian(itater):
   global prior_file
   element_dict = { \
      0:'Bq', 1:'H', 6:'C', 7:'N', 8:'O', 9:'F', 14:'Si', 16:'S', 17:'Cl', 25:'Mn', 26:'Fe', 27:'Co', 44:'Ru'}
   RE1 = re.compile('Standard orientation:')
   RE2 = re.compile(' --------')

   numatoms = 0; numgeoms = 0
   outdata = []
   for x in itater:
      if RE1.search(x):
         if prior_file:
            prior_file = False
            continue
         numgeoms += 1
         [next(itater) for i in range(4)]
         while True:
            t = next(itater)
            if RE2.match(t):
               break
            else:
               if numgeoms == 1: numatoms += 1
               rawdata = t.split()
               outstring = '{}   {}  {}  {}'.format(element_dict[int(rawdata[1])], rawdata[3], rawdata[4], rawdata[5])
               outdata.append(outstring)
   return numatoms, numgeoms, outdata

# User definitions
title = 'Optimization step '

infile = open(sys.argv[1], 'r')
data = iter(infile.readlines())
infile.close()

prior_file = False
if exists('optimization.xyz'):
   prior_file = True
   copyfile('optimization.xyz', 'optimization.xyz.bak')
   f = open('optimization.xyz', 'r')
   t = f.readlines()
   f.close()
   for i in t:
      if RE3.match(i):
         step = int(i.split()[1])
else:
   step = 0  # To index optimization with structure, since RE1 occurs once before step 1

for x in data:
   if RE4a.search(x):
      numatoms, numgeoms, geomlist = qchem(data)
   elif RE4b.search(x):
      numatoms, numgeoms, geomlist = gaussian(data)

outfile = open('optimization.xyz', 'a+')
for i in range(numgeoms):
   # Check whether this is ongoing optimization. If so, don't write first structure, as this is just
   #    last structure of previous optimization run.
   step += 1
   outfile.write(str(numatoms) + '\n')
   outfile.write('Step {} of geometry optimization\n'.format(step))
   for j in range(numatoms):
      outfile.write(geomlist[numatoms*i + j] + '\n')
outfile.close()
