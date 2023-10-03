#!/usr/bin/env python
# Script to add or subtract z vacuum gap to Crystalmaker material supercell.

import re, math
import numpy

# User input
input_structure_filename = 'test2.cmtx'
output_structure_filename = 'test3.cmtx'

# How much vacuum does the user want normal to the surface?
vacuum_depth = 10.0 # Angstroms

RE1 = re.compile('CELL')
RE2 = re.compile('ATOM')
atom_dict = {}  # Entries 1-index:numpy.array(x,y,z)

file = open(input_structure_filename, 'r')
data = file.readlines()
file.close()

file = open(output_structure_filename, 'w')

# Get old cell dimension from Crystalmaker data
for i in data:
   if RE1.match(i):
      a_axis_length = float(i.split()[1])
      b_axis_length = float(i.split()[2])
      c_axis_length_old = float(i.split()[3])
      alpha = math.radians(float(i.split()[4]))
      beta = math.radians(float(i.split()[5]))
      gamma = math.radians(float(i.split()[6]))

# First, create atom dictionary with coordinates
min_c = 1.0
for i in xrange(len(data)):
   if RE2.match(data[i]):   # This loop changes individual fractional coordinates
      j = 0; switch = True
      while switch:
         j += 1
         if len(data[i+j]) > 2:  # Arbitrary length limit, just to eliminate blank line at end
            t = data[i+j].split()
            (a,b,c) = tuple([float(k) for k in t[2:5]]) 
            atom_dict[j] = numpy.array([a, b, c])
            if c < min_c: min_c = c
         else:
            switch = False

# Now shift all c values down by the minimum value
for i in atom_dict:
   atom_dict[i][2] -= min_c

print 'min_c before shift: ' + str(min_c)

# Convert fractional coordinate axes to Cartesian.
volume = math.sqrt(1. - math.pow(math.cos(alpha),2) - math.pow(math.cos(beta),2) - \
   math.pow(math.cos(gamma),2) + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
T11 = a_axis_length
T12 = b_axis_length*math.cos(gamma)
T13 = c_axis_length_old*math.cos(beta)
T21 = 0.
T22 = b_axis_length*math.sin(gamma)
T23 = c_axis_length_old*((math.cos(alpha) - math.cos(beta)*math.cos(gamma))/math.sin(gamma))
T31 = 0.
T32 = 0.
T33 = c_axis_length_old*volume/math.sin(gamma)

trans = numpy.matrix([ [T11, T12, T13], [T21, T22, T23], [T31, T32, T33] ])

# Fractional coordinate axes are just 1 0 0 etc. in cell coordinate system
#a_frac = numpy.matrix( [1., 0., 0.] ).T
#b_frac = numpy.matrix( [0., 1., 0.] ).T
c_axis_frac = numpy.matrix( [0., 0., 1.] ).T

# Now express these in Cartesian space with actual cell dimensions
#a_cart = trans*a_frac#; print a_cart
#b_cart = trans*b_frac#; print b_cart
c_axis_cart = trans*c_axis_frac ; print 'c_axis_cart[2,0] = ' + str(c_axis_cart[2,0])

# Even for oblique cell, cell should be defined with a and b along base (no vacuum component along these axes)
# So, just need to extend the c axis until z projection is as desired

# What is the maximum z value?
max_c = 0.0
for i in atom_dict:
   if atom_dict[i][2] > max_c: max_c = atom_dict[i][2]
max_z = trans*numpy.matrix( [0., 0., max_c] ).T; max_z = max_z[2,0]

print 'max_c after shift = ' + str(max_c)
print 'max_z = ' + str(max_z)

# What is the vacuum gap?
vacuum = c_axis_cart[2,0] - max_z

# What is the difference between the desired gap and the actual one?
gap_diff = vacuum_depth - vacuum

# Now need to scale the cell c axis to make the desired vacuum
extension_factor = (c_axis_cart[2,0] + gap_diff)/c_axis_cart[2,0]
c_axis_cart_new = c_axis_cart * extension_factor
c_axis_length_new = numpy.linalg.norm(c_axis_cart_new)

# Scale fractional c coordinates for new cell size
for i in atom_dict:
   atom_dict[i][2] = atom_dict[i][2] * 1./extension_factor

# Write out data into new CMTX file.
switch = False
for i in xrange(len(data)):
   if RE1.match(data[i]):    # This changes unit cell dimensions
      t = data[i].rstrip().split()
      t[3] = c_axis_length_new
      file.write('%-5s' % t[0])
      file.write('%10.6f%10.6f%10.6f%11.6f%11.6f%11.6f\n' % \
       tuple( [float(j) for j in t[1:]]))
      continue
   elif RE2.match(data[i]):   # This loop changes individual fractional coordinates
      switch = True
      file.write(data[i])
      for j in range(len(atom_dict)):
         t = data[i + j + 1].strip().split()
         file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (t[0], t[1], atom_dict[j+1][0], \
                    atom_dict[j+1][1], atom_dict[j+1][2]))
   if switch == True:
      file.write('\n')  # Write blank line at end of file
      break
   else:
      file.write(data[i])
file.close()
