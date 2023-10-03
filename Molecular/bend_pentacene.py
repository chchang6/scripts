#!/usr/bin/env python
# Script to bend pentacene by user-specd angle. CHC 03/29/12
# Input and output standard XYZ format

import numpy
import math

def translate(coord_set, translation_vector):
   a = numpy.zeros_like(coord_set)
   for i in xrange(numpy.shape(a)[0]):
      a[i,:] = coord_set[i,:] + translation_vector
   return a

def crossprod(vector1, vector2):
   matrix_i = numpy.array([[vector1[1], vector1[2]], [vector2[1], vector2[2]]])
   matrix_j = numpy.array([[vector1[0], vector1[2]], [vector2[0], vector2[2]]])
   matrix_k = numpy.array([[vector1[0], vector1[1]], [vector2[0], vector2[1]]])
   det_i = numpy.linalg.det(matrix_i)
   det_j = numpy.linalg.det(matrix_j)
   det_k = numpy.linalg.det(matrix_k)
   return numpy.array([det_i, -1.*det_j, det_k])

def rotate_x(coord_set, angle_radians):
   a = numpy.asmatrix(coord_set)
   b = numpy.matrix([ [1., 0., 0.], \
       [0., math.cos(angle_radians), -1.*math.sin(angle_radians)], \
       [0., math.sin(angle_radians), math.cos(angle_radians)]])
   return a*b

def rotate_z(coord_set, angle_radians):
   a = numpy.asmatrix(coord_set)
   b = numpy.matrix([ [math.cos(angle_radians), -1.*math.sin(angle_radians), 0.], \
       [math.sin(angle_radians), math.cos(angle_radians), 0.], \
       [0., 0., 1.] ])
   return a*b

def dump_work(coord_set):
   # For debugging
   outfile = open('dump.xyz', 'w')
   outfile.write(str(numpy.shape(coord_set)[0]) + '\n')
   outfile.write('Debug dump\n')
   for i in xrange(len(coord_set)):
      outfile.write('%-5s%11.6f%11.6f%11.6f\n' % (start_data_dict[i+1][0], working_coords[i,0], \
         working_coords[i,1], working_coords[i,2]))
   outfile.close()
   return

# All atomic indices one-indexed.
angle_to_bend = 45.  # In degrees
indices_to_bend = (1,2,5,6,9,10,13,14,17,18,25,26,29,30,33,34)
bridgehead_C_indices = (21,22)

file = open('planar.xyz', 'r')
data = file.readlines()
file.close()

start_data_dict = {}
for i in range(2,len(data)):
   t = data[i].strip().split()
   start_data_dict[i-1] = (t[0], numpy.array([float(j) for j in t[1:]]))

# Create working array
working_coords = numpy.zeros((len(start_data_dict), 3), numpy.float)
for i in xrange(len(start_data_dict)):
   working_coords[i,0:3] = start_data_dict[i+1][1]

# Current centroid
current_centroid = (working_coords[bridgehead_C_indices[0]-1] + working_coords[bridgehead_C_indices[1]-1])/2.
# Translate molecule so centroid @ origin
working_coords = translate(working_coords, -1.*current_centroid)
#dump_work(working_coords)
# Now rotate so bridgehead carbons are in XY plane, if necessary
positive_unit_x = numpy.array([1.,0.,0.])
bridgehead_atom1_z = working_coords[bridgehead_C_indices[0]-1][2]
if math.fabs(bridgehead_atom1_z) > 1e-6:
   vec1 = [0., 0., 1.]
   vec2 = crossprod( numpy.ravel(working_coords[bridgehead_C_indices[0]-1]) ,numpy.array([1.,0.,0]) )
   theta_rads = math.acos(numpy.vdot(vec1,vec2) / numpy.linalg.norm(vec2))
   # Rotate system about x axis to bring first bridgehead carbon into XY plane
   working_coords = rotate_x(working_coords,theta_rads)
# Need "ravel" here to flatten from [[row]] to [row]
theta_rads = -1.*math.acos(numpy.vdot(positive_unit_x, numpy.ravel(working_coords[bridgehead_C_indices[0]-1,:]) ) / \
   numpy.linalg.norm(working_coords[bridgehead_C_indices[0]-1,:]))
working_coords = rotate_z(working_coords, theta_rads)

# Now the "tricky" part. Rotate atoms in indices_to_bend around x by theta, leaving the rest fixed.
# First, set up coordinate matrix with just those atoms.
moving_coords = numpy.zeros((len(indices_to_bend), 3), numpy.float)
for i in xrange(len(indices_to_bend)):
   moving_coords[i,:] = working_coords[indices_to_bend[i]-1, :]
moving_coords = rotate_x(moving_coords, math.radians(angle_to_bend))
# Reassemble coordinates and dump to outfile
for i in xrange(len(indices_to_bend)):
   working_coords[indices_to_bend[i]-1, :] = moving_coords[i,:]
outfile = open('test.xyz', 'w')
outfile.write(str(len(start_data_dict)) + '\n')
outfile.write('Pentacene bent about bridgehead at ' + str(angle_to_bend) + ' degrees\n')
for i in xrange(len(start_data_dict)):
   outfile.write('%-5s%11.6f%11.6f%11.6f\n' % (start_data_dict[i+1][0], working_coords[i,0], \
    working_coords[i,1], working_coords[i,2]))
outfile.close()
