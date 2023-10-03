#!/usr/bin/env python
# Script to automatically extract relaxed structures from Gaussian
#   coordinate scan, fit to quadratic function over specified data range,
#   and create XYZ trajectory file.
# User can modify fitting function to fit from 0 displacement (molecule
#   behaves as ideal spring) as ax^2, or from arbitrary displacement as
#   ax^2 + bx + c (harmonic region only comes after some stretch).
# If assume spring energy is 1/2*kx^2, force is kx, force constant is k
#   1 kcal/mol/A2 * 4.184 kJ/kcal * 1000 N*m/kJ * 1e10 A/m * 1e12 pN/N / 6.022e23 molecules/mole = 69.48 pN/mol/A

from os import listdir
from math import sqrt
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

RE2 = re.compile('YES')
RE3a = re.compile('Z-Matrix orientation')
RE3b = re.compile('Standard orientation')
RE4 = re.compile('NAtoms')
RE5 = re.compile('Conve')
RE6 = re.compile('SCF Done')
RE7 = re.compile(' Optimization completed on the basis of negligible forces.')

kcal_to_pN = 69.48

# User modifications
# The following two global variables are the 1-indexed atom numbers
#   used to define the displacement
RE1 = re.compile('2b{0,1}\.log')
atom_ref_index1 = 76
atom_ref_index2 = 78
# Output files
force_plot_FN = 'force_OO.png'
trajectory_FN = 'trajectory_OO.xyz'
# Which fit and data range
fit_full_quadratic = True
fit_range = (3,18)  # Number of points, not values
# Coordinates to place force constant
(FC_x, FC_y) = (0.1, 90)

element_dict = { \
   0:'Bq', 1:'H', 6:'C', 7:'N', 8:'O', 16:'S', 17:'Cl', 26:'Fe', 44:'Ru'}

def convtest(datalist,linenum):
   if RE2.search(datalist[linenum+1]) and \
      RE2.search(datalist[linenum+2]) and \
      RE2.search(datalist[linenum+3]) and \
      RE2.search(datalist[linenum+4]):
      return True
   elif RE7.match(datalist[linenum+6]):
      return True
   else:
      return False

def get_energy(datalist, linenum):
   # Move backward through data to line with energy
   # SCF Done:  E(RPM6) =  0.574578652040     A.U. after   12 cycles
   shift = 1
   while True:
      if RE6.search(datalist[linenum-shift]):
         t = datalist[linenum-shift].split('=')
         energy = float(t[1].split()[0])
         break
      else: shift += 1
   return energy

def get_structure(datalist, linenum, energy):
   # Coordinates start 5 lines past linenum, and go for numatoms
   atoms = []
   for i in xrange(5, numatoms+5):
      t = datalist[linenum+i].strip().split()
      element = element_dict[int(t[1])]
      x = float(t[3])
      y = float(t[4])
      z = float(t[5])
      atoms.append([element, x, y, z])
   ref_atom1 = atoms[atom_ref_index1-1]
   ref_atom2 = atoms[atom_ref_index2-1]
   displacement = round( sqrt( (ref_atom2[1] - ref_atom1[1])**2 + \
                               (ref_atom2[2] - ref_atom1[2])**2 + \
                               (ref_atom2[3] - ref_atom1[3])**2), 3)
   return(atoms, displacement, energy)

def quad_fit(x, a, *bc):
   # bc will come as a pair if it comes at all.
   try:  # If bc there, we want the full quadratic
      bc[0]
      return 0.5*a*np.square(x) + bc[0]*x + bc[1]
   except IndexError:  # We only got a
      return 0.5*a*np.square(x)

files = listdir('.')
newfiles = []
for i in files:
   if RE1.search(i): newfiles.append(i)
# Following special hack to move _b.log to front of list.
#newfiles.insert(0,newfiles.pop())
files = newfiles

optimized_structures = {}

for i in files:
   found_numatoms = False
   file = open(i, 'r')
   print 'Analyzing file ' + i
   data = file.readlines()
   file.close()
   for j in xrange(len(data)):
      if RE4.search(data[j]) and found_numatoms == False:
         #print 'Found NAtoms string: ' + data[j]
         t = data[j].split()
         #print 'Assuming this is a number: ' + t[1]
         numatoms = int(t[1])
         found_numatoms = True
      elif RE5.search(data[j]):
         if convtest(data,j):
            E = get_energy(data,j)
            k = 0
            while True:
               t = data[j+k]
               if RE3a.search(t) or RE3b.search(t):
                  structure = get_structure(data, j+k, E)  # (atoms, disp, E)
                  optimized_structures[structure[1]] = structure
                  break
               else: k += 1

# Arrange keys in order, relate absolute to relative displacements
# rel_disps = [(0.0, 12.3), (0.1, 12.4), etc)]
struct_keys = optimized_structures.keys()
struct_keys.sort()
ref_displacement = struct_keys[0]
rel_disps = []
for i in xrange(len(struct_keys)):
   rel_disps.append( ((struct_keys[i] - ref_displacement), struct_keys[i]) )

# Dump file of structures
outfile = open(trajectory_FN, 'w')
for i in range(len(struct_keys)):
   outfile.write(str(numatoms) + '\n')
   outfile.write('Energy = %12.6f Ha\n' % optimized_structures[struct_keys[i]][2])
   for j in optimized_structures[struct_keys[i]][0]:
      outfile.write('%2s      %10.6f%10.6f%10.6f\n' % tuple(j))
outfile.close()

x = []
y = []
ref_energy = optimized_structures[rel_disps[0][1]][2]
#print 'Reference energy ' + str(ref_energy)
print 'Displacement (A)\tRel. Energy (kcal/mol)'
for i in rel_disps:
   x.append(i[0])
   # i[1] is an absolute displacement, so first term is energy of nth item in rel_disps
   # rel_disps[0][1] is the absolute displacement of the unperturbed system.
   my_energy = optimized_structures[i[1]][2]
   #print 'My energy ' + str(my_energy)
   y.append(627.51 * (my_energy - ref_energy))
   print '%9.3f		%12.3f' % (x[-1], y[-1])

x = np.asarray(x)
y = np.asarray(y)
# Fit y data to quadratic 1/2*ax^2 or full 1/2*ax^2 + bx + c if minimum displaced
if fit_full_quadratic == False:
   (opt, cov) = optimize.curve_fit(quad_fit, x[fit_range[0]:fit_range[1]], y[fit_range[0]:fit_range[1]], p0=[1.])
   yfit = quad_fit(x, opt[0])
   Fquad = opt[0]*x
else:
   (opt, cov) = optimize.curve_fit(quad_fit, x[fit_range[0]:fit_range[1]], y[fit_range[0]:fit_range[1]], p0=[1.,1.,0.])
   yfit = quad_fit(x, opt[0], opt[1], opt[2])
   Fquad = opt[0]*x + opt[1]

print 'Force constant is ' + str(opt[0]) + ' kcal/(mol-A**2)'
print 'Force constant is ' + str(kcal_to_pN*opt[0]) + ' pN/A)'

fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
ser1 = plot1.plot(x, y, label='Calculated')
if fit_full_quadratic:
   ser2 = plot1.plot(x, yfit, label='Fit $ \\frac{1}{2}ax^2 + bx + c $')
else:
   ser2 = plot1.plot(x, yfit, label='Fit $\frac{1}{2}ax^2$')
ser3 = plot1.plot(x, Fquad, label='Force (kcal/mol/A2)')
plt.setp(ser1, color='k', marker='s')
plt.setp(ser2, color='r')
plt.setp(ser3, color='g')
plot1.set_title('Ru tris-bpy O-O stretch')
plot1.set_xlabel('O76-O78 displacement from minimum-energy structure (${\AA}$)')
plot1.set_ylabel(r'Relative energy ($\frac{kcal}{mol}$)')
#plot1.set_ylim(top=25)
plot1.legend(loc='upper left')
plot1.text(FC_x, FC_y, 'a = %6.2f pN/A' % (kcal_to_pN*opt[0]) )
fig1.savefig(force_plot_FN)

# Create G09 file for ZINDO calculations
#outfile = open('ZINDO.gjf', 'w')
#outfile.write('%Chk=ZINDO.chk\n%NProcShared=8\n\n')
#for i in rel_disps:
#   if i == rel_disps[0]:
#      outfile.write('#P ZIndo(Singlets, NStates=5)\n\n')
#   #elif round(i[0],1) >= 1.7:
#   #   outfile.write('#P ZIndo(Singlets, NStates=5) SCF=QC Guess=Read Stable=Opt\n\n')
#   else:
#      outfile.write('#P ZIndo(Singlets, NStates=5) Guess=Read\n\n')
#   outfile.write('ZINDO calculation for ' + str(i[0])[0:5] + ' Ang displacement\n\n')
#   outfile.write('1 6\n')
#   for j in optimized_structures[i[1]][0]:
#      outfile.write('%-5s%12.6f%12.6f%12.6f\n' % (j[0], j[1], j[2], j[3]))
#   outfile.write('\n--Link1--\n%Chk=ZINDO.chk\n\n')
#outfile.close()
