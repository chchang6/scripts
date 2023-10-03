#!/usr/bin/env python
# Script to take 2 X 3 sets of atomic coordinates and calculate dihedral angle
#   between planes defined by each triplet of atoms.

import numpy

# Definition of first plane. atom2 forms middle of angle.
atomvec1 = numpy.array(X,Y,Z)
atomvec2 = numpy.array(X,Y,Z)
atomvec3 = numpy.array(X,Y,Z)
bond_vector1 = atomvec1 - atomvec2
bond_vector2 = atomvec3 - atomvec2
vec1 = numpy.cross(bond_vector1, bond_vector2)
norm1 = linalg.norm(vec1)

# Definition of second plane. atom5 forms middle of angle.
atomvec4 = numpy.array(X,Y,Z)
atomvec5 = numpy.array(X,Y,Z)
atomvec6 = numpy.array(X,Y,Z)
bond_vector3 = atomvec4 - atomvec5
bond_vector4 = atomvec6 - atomvec5
vec2 = numpy.cross(bond_vector1, bond_vector2)
norm2 = linalg.norm(vec2)

# Calculate dihedral angle
angle = numpy.arccos(numpy.vdot(vec1, vec2) / (norm1 * norm2))[0]

# Project bond_vector3 onto vec1 to determine sign. If dot product is negative,
#   then the dihedral is positive, and vice versa. 180 degrees may fail due to
#   numerical precision.
#   sign = 1.
#   if numpy.vdot(vec1, bond_vector3) > 0.: sign = -1.
#   return sign * angle * 180 / numpy.pi

print angle * 180. / numpy.pi

