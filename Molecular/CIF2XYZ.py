#!/usr/bin/python
# Script to create an XYZ-format file from CIF. Searches for
# necessary information via string comparison, gets it by slicing,
# prompts user for unit cell repeat in +/- xyz, then calculates
# required coordinates and dumps. CHC
import os
import sys
import re
from math import *
from numpy import *
# Create regular expression pattern to remove parenthetical errors
# and to detect blank lines.
error = re.compile(r"\([0-9]*\)")
blankline = re.compile(r"^\ *$")
# Get input line arguments
if (len(sys.argv) == 1) or (sys.argv[1] == 'help'):
   print 'Format is ./CIF2XYZ name_infile'
   print 'Will output name_infile_basename.out.'
   sys.exit()
else:
   name_infile=sys.argv[1]
   templist=os.path.splitext(name_infile)
   if templist[1] != '.cif':
      print 'Please ensure file is in CIF format, and has a .cif extension'
      sys.exit()
   if os.path.isfile('templist[0].xyz'):
      print templist[0] + '.xyz already exists! Please move or delete before running this program.'
      sys.exit()
infile = open(name_infile, 'r')
I = infile.readlines()
# Get crystal unit cell parameters
for i in I:
   test = i.split()
   if len(test) < 1:
      continue
   elif test[0] == "_symmetry_space_group_name_H-M":
      HMspace_group=test[1]
   elif test[0] == '_cell_length_a':
      a = float(error.sub(r'',test[1]))
   elif test[0] == '_cell_length_b':
      b = float(error.sub(r'',test[1]))
   elif test[0] == '_cell_length_c':
      c = float(error.sub(r'',test[1]))
   elif test[0] == '_cell_angle_alpha':
      alpha_deg = float(error.sub(r'',test[1]))
      alpha = radians(alpha_deg)
   elif test[0] == '_cell_angle_beta':
      beta_deg = float(error.sub(r'',test[1]))
      beta = radians(beta_deg)
   elif test[0] == '_cell_angle_gamma':
      gamma_deg = float(error.sub(r'',test[1]))
      gamma = radians(gamma_deg)
# Get asymmetric unit in fractional coordinates. Create lists
# element, asym_x, asym_y, asym_z
elements=[]
asym_x=[]
asym_y=[]
asym_z=[]
j = I.index(' _atom_site_disorder_group \n')
while j:
   temp1 = I[j+1].split()
   if temp1 == []: break;
   else:
      elements.append(temp1[1])
      asym_x.append(float(error.sub(r'',temp1[2])))
      asym_y.append(float(error.sub(r'',temp1[3])))
      asym_z.append(float(error.sub(r'',temp1[4])))
   j += 1
# Create coordinate array for asymmetric unit
asym = empty( (len(elements),3) )
asym[:,0] = asym_x
asym[:,1] = asym_y
asym[:,2] = asym_z
# Done acquiring necessary input. Get unit cell repeat from user.
#print 'Please enter the desired unit cell repeats for +a, -a, +b, -b, +c, and -c'
#print 'as list of format "+a -a +b -b +c -c". If only the unit cell is desired,'
#print 'enter "0 0 0 0 0 0".'
#repeatlist = sys.stdin.read().split(' ')
# 
# Generate unit cell. This will be an array with sets of 3 columns
# specifying (x,y,z) coordinates defined by their respective generating
# operation from the asymmetric unit. One row per atom in the asymmetric
# unit. Use the length of the first column in array asym (element list in
# asymmetric unit) as counter limit.
if HMspace_group == 'P-1':
   unit = empty( (len(elements),3) )
   num_symmetries = 1
   unit = -asym
# Generate full unit cell coordinate structure. N X 3g array of coordinates.
# Each row is an element; g = num_symmetries + 1.
fullunit = asym
i = 0
while i <= num_symmetries-1:
   temp_array = unit[:,3*i:3*i+3]
   fullunit = concatenate((fullunit,temp_array), 1)
   i += 1
# Transform to Cartesian coordinates
V = alpha*beta*gamma*sqrt(1-pow(math.cos(alpha),2)-
                            pow(math.cos(beta),2)-
                            pow(math.cos(gamma),2)+
                            2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
#Minv = array([[a,b*math.cos(gamma),c*math.cos(beta)],
#             [0.,b*math.sin(gamma),c*(math.cos(alpha)-math.cos(beta)*math.cos(gamma))/math.sin(gamma)],
#             [0.,0.,V/(a*b*math.sin(gamma))]])
delta=math.acos((math.cos(gamma)-math.cos(alpha)*math.cos(beta))/(math.sin(alpha)*math.sin(beta)))
Minv = array([[a*math.sin(beta),b*math.sin(alpha)*math.cos(delta),0.],
             [0.,b*math.sin(alpha)*math.sin(delta),0.],
             [a*math.cos(beta),b*math.cos(alpha),c]])
Minv_matrix = matrix(Minv)
outfile = open(str(templist[0])+".xyz", 'w')
num_unitcells = 1
num_atoms = num_unitcells*asym.shape[0]*(num_symmetries+1)
outfile.write(str(num_atoms))
outfile.write("\n\n")
i = 0 # Number of atoms in asymmetric unit
j = 0 # Number of unit cell symmetries + 1
while i < asym.shape[0]:
   while j <= (num_symmetries):
      crystallographic = matrix(fullunit[i,3*j:3*j+3])
      cartesian = Minv_matrix*crystallographic.T
      outfile.write(elements[i]+' '+str(cartesian.T)+"\n")
      j = j+1
   j = 0
   i = i+1
outfile.close()
