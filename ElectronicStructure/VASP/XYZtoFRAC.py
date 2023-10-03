#!/usr/bin/env python
# Script to convert XYZ to VASP POSCAR given supercell dimensions.

import re, math
import numpy

class renderpar:
   def __init__(self, e, rad, r, g, b):
      self.element = e # (string)
      self.radius = rad # (float)
      self.red = r # (float)
      self.green = g # (float)
      self.blue = b # (float)
   def get_element(self):
      return self.element
   def get_radius(self):
      return self.radius
   def get_red(self):
      return self.red
   def get_green(self):
      return self.green
   def get_blue(self):
      return self.blue

# User definitions
# Set unit cell parameters from presumed material supercell
a =  11.517000
b = 11.517000
c = 27.640801
alpha = math.radians(90.000000)
beta = math.radians(90.000000)
gamma = math.radians(90.000000)

# Shifts in fractional coordinates from origin
a_shift = 0.5
b_shift = 0.5
c_shift = 0.7

# Rendering parameters
atom_dict = {'C': renderpar('C', 0.29, 0.06577, 0.02538, 0.00287), \
             'H': renderpar('H', 0.10, 1.00000, 0.74243, 0.74243), \
             'O': renderpar('O', 1.21, 1.00000, 0.00000, 0.00000), \
             'Pd': renderpar('Pd', 0.78, 0.75978, 0.76817, 0.72453), \
             'Ir': renderpar('Ir', 0.77, 0.78975, 0.81032, 0.45048) }

file = open('temp.xyz', 'r')
data = file.readlines()
file.close()
numatoms = int(data[0].strip())
elements = []
coors = []
for i in range(2,numatoms+2):
   t = data[i].rstrip().split()
   elements.append(t[0])
   coors.append([float(j) for j in t[1:]])

# Calculate volume of cell
volume = math.sqrt(1. - math.pow(math.cos(alpha),2) - math.pow(math.cos(beta),2) - \
   math.pow(math.cos(gamma),2) + 2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))

# Define elements of transformation matrix, see http://en.wikipedia.org/wiki/Fractional_coordinates#Conversion_to_cartesian_coordinates
T11 = 1/a
T12 = -math.cos(gamma)/(a*math.sin(gamma))
T13 = (math.cos(alpha)*math.cos(gamma)-math.cos(beta))/(a*volume*math.sin(gamma))
T21 = 0.
T22 = 1/(b*math.sin(gamma))
T23 = (math.cos(beta)*math.cos(gamma)-math.cos(alpha))/(b*volume*math.sin(gamma))
T31 = 0.
T32 = 0.
T33 = math.sin(gamma)/(c*volume)

T = numpy.array([ [T11, T12, T13], [T21, T22, T23], [T31, T32, T33] ])

# Now set up Cartesian coordinates
#   coors is 3 X N, with rows representing x, y, and z values
Cartesians = numpy.asmatrix(coors).T

# Transform
Fractional = T*Cartesians

# Assume molecule is origin-centered.
# Shift up 1/2 a unit cell along a, b, and c (a and b to center on surface, 
#   c b/c surface occupying the lower half of cell
for i in xrange(numpy.shape(Fractional)[1]):
   Fractional[0,i] += a_shift
   Fractional[1,i] += b_shift
   Fractional[2,i] += c_shift

# Write out section that can be pasted into CMTX file.
#   template Pd  Pd1     0.750000 0.750000 0.333333
file = open('test.frac', 'w')
for i in xrange(numpy.shape(Fractional)[1]):
   file.write('%-4s%-7s%9.6f%9.6f%9.6f\n' % (elements[i], elements[i]+'1', Fractional[0,i], Fractional[1,i], Fractional[2,i]))
# For convenience, output rendering information
#   Template "Pd    0.78  0.75978 0.76817 0.72453", element, radius, RGB
element_set = set(elements)
for i in element_set:
   file.write('%-2s%8.2f %8.5f%8.5f%8.5f\n' % (atom_dict[i].get_element(), \
   atom_dict[i].get_radius(), atom_dict[i].get_red(), atom_dict[i].get_green(), \
   atom_dict[i].get_blue()))
file.close()
