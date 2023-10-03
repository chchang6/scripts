#!/usr/bin/env python
# Script to create XYZ movie file from concatenated OUTCAR files.
# If there are multiple restarts, create single OUTCAR by e.g.,
#   cat OUTCAR.1 OUTCAR.2 ... > OUTCAR
# Example usage "./catOUTCAR.py movie.xyz"

import sys, re, os
import gzip
import numpy

def getFirstGeom():
   Geom = []
   while True:
      x = file.readline()
      if re.match('\n', x): break
      else:
         g = x.split()
         Geom.append((float(g[0]), float(g[1]), float(g[2])))
   return Geom

def getGeom():
   Geom = []
   while True:
      x = file.readline()
      if re.search('-----', x): break
      else:
         g = x.split()
         Geom.append((float(g[0]), float(g[1]), float(g[2])))
   return Geom
         
RE1 = re.compile('free  energy')
RE2 = re.compile(' POSITION')
RE3 = re.compile('   ions per type =')
RE4 = re.compile(' POTCAR:')
RE5 = re.compile(' position of ions in cartesian coordinates  (Angst)')
RE6 = re.compile(r'OUTCAR\.[0-9]+\.gz')

gotElements = False
gotNumElements = False
gotFirstGeom = False

Elements = []
NumElements = []
coors = []
energies = []
# Find out the indices of OUTCAR.#.gz files are present
files = os.listdir('.')
OUTCAR_indices = []
for i in files:
   if RE6.match(i):
      t1 = i.rstrip('.gz')
      t2 = t1.lstrip('OUTCAR.')
      OUTCAR_indices.append(int(t2))
OUTCAR_indices.sort()

# Get coordinates
for i in OUTCAR_indices:
   file = gzip.open('OUTCAR.'+str(i)+'.gz', 'r')
   while True:
      x = file.readline()

      if x == '': break
   # Will repeat this process for each outer loop iteration, although not necessary,
   #   to keep changes minimal.
      if not gotElements and RE4.match(x):
         temp = x.split(':')
         temp = temp[1].split()
         if temp[1] not in Elements: Elements.append(temp[1])
         else: gotElements = True

      if not gotNumElements and RE3.match(x):
         numAtoms = 0
         temp = x.split('=')
         temp = temp[1].split()
         for i in temp:
            NumElements.append(int(i))
            numAtoms += int(i)
         gotNumElements = True
# If input right, get geometry. Either the first geometry block, or a subsequent one.
      if not gotFirstGeom and RE5.match(x):
         coors.append(getFirstGeom())
         gotFirstGeom = True
      else:
         if RE2.match(x):
            file.readline() # Skip first border of dashes
            coors.append(getGeom())
# If input right, get corresponding energy.
      if RE1.search(x):
            temp = x.split('=')
            energies.append(temp[1])
   file.close()
# Create dumb list of atom types for later
atomtypes = []
for i in xrange(len(NumElements)):
   for j in xrange(NumElements[i]):
      atomtypes.append(Elements[i])
outfile = open(sys.argv[1], 'w')
strnumatoms = str(numAtoms) + '\n'
counter = 0
for i in xrange(len(coors)):
   outfile.write(strnumatoms)
   outfile.write('Frame ' + str(counter+1) + ' Energy' + energies[counter])
   for j in xrange(numAtoms):
      outfile.write('%-5s%10.6f%10.6f%10.6f\n' % (atomtypes[j], coors[i][j][0], coors[i][j][1], coors[i][j][2]))
   counter += 1
outfile.close()
