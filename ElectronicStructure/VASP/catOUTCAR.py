#!/usr/bin/env python
# Script to create XYZ movie file from concatenated OUTCAR files.
# If there are multiple restarts, create single OUTCAR by e.g.,
#   cat OUTCAR.1 OUTCAR.2 ... > OUTCAR
# Example usage "./catXDAT.py movie.xyz"

import sys, re
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

gotElements = False
gotNumElements = False
gotFirstGeom = False
gotLattice = False

Elements = []
NumElements = []
coors = []
energies = []
# Get coordinates
if len(sys.argv) == 3:
   file = open(sys.argv[1], 'r')
elif len(sys.argv) == 2:
   file = open('OUTCAR', 'r')
else:
   sys.exit('Usage: catOUTCAR.py [OUTCAR_file] XYZ_file')

while True:
   x = file.readline()

   if x == '': break

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
#    coors is nested list, coors[frame][atom][x=0|y=1|z=2]
   if not gotFirstGeom and RE5.match(x):  # First geometry
         coors.append(getFirstGeom())
         gotFirstGeom = True
   else: # Subsequent geometries
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
outfile = open(sys.argv[-1], 'w')
strnumatoms = str(numAtoms) + '\n'
counter = 0
for i in xrange(len(coors)):
   outfile.write(strnumatoms)
   outfile.write('Frame ' + str(counter+1) + ' Energy' + energies[counter])
   for j in xrange(numAtoms):
      x = coors[i][j][0]
      y = coors[i][j][1]
      outfile.write('%-5s%10.6f%10.6f%10.6f\n' % (atomtypes[j], x, y, coors[i][j][2]))
   counter += 1
outfile.close()
