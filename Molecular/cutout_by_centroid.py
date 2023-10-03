#!/usr/bin/env python

import sys, math, os
import numpy
#numpy.set_printoptions(threshold=numpy.nan)
from scipy.linalg import norm
from time import time

class Atom:
   __name__ = 'Atom'
   def __init__(self, e, x, y, z):
      self.element = e
      self.x = x
      self.y = y
      self.z = z
      return
   def get_x(self):
      return self.x
   def get_y(self):
      return self.y
   def get_z(self):
      return self.z
   def get_coors(self):
      return numpy.array([self.x, self.y, self.z])
   def get_element(self):
      return self.element

def get_molecule(atom_index_list, threshold):
   called_ind = set(atom_index_list)
   #print 'get_molecule called with ' + str(called_ind)
   for i in atom_index_list:
      test = distances[i, :]
      indices_thismol = list(numpy.where(test <= threshold)[0])
      atom_index_list.extend([j for j in indices_thismol if j not in set(atom_index_list)])
      #print atom_index_list
   new_ind = set(atom_index_list)
   #print 'get_molecule new index list is ' + str(new_ind)
   if len(called_ind) == len(new_ind):  # No new indices, we are done
      return list(new_ind)
   else:
      return get_molecule(list(new_ind), threshold)

def testdump(filename, numatoms, atomlist):
   outfile = open(filename, 'w')
   outfile.write(str(numatoms) + '\n\n')
   for i in atomlist:
      outfile.write('%5s%12.6f%12.6f%12.6f\n' % (i.get_element(), i.get_x(), i.get_y(), i.get_z()))
   outfile.close()
   return

print('Reading XYZ file')
file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

numatoms = int(data[0].strip())
atoms = []

print 'Creating Atom list' 
for i in range(2, numatoms+2):
   t = data[i].strip().split()
   atoms.append(Atom(t[0], float(t[1]), float(t[2]), float(t[3])))

print('Creating atomic distance matrix...'),
sys.stdout.flush()
# Distance matrix is full so can just pull row to get all distances.
if os.access('/Users/cchang/Desktop/distance_matrix.npy', os.R_OK):
   file = open('/Users/cchang/Desktop/distance_matrix.npy', 'r')
   distances = numpy.load(file)
   file.close()
else:
   distances = numpy.zeros( (numatoms, numatoms), numpy.float )
   # Algorithm 1: explicit loop
   #start_time = time()
   #for i in xrange(len(atoms)):
   #   for j in range(i+1, len(atoms)):
   #      distances[i,j] = norm(atoms[i].get_coors() - atoms[j].get_coors())
   #      distances[j,i] = distances[i,j]
   #end_time = time()
   # Algorithm 2: Build XYZ array, then index into it
   start_time = time()
   coors_array = numpy.zeros( (len(atoms), 3), numpy.float)
   for i in xrange(len(atoms)):
      coors_array[i, :] = atoms[i].get_coors()
   for i in xrange(len(atoms)):
      for j in range(i+1, len(atoms)):
         distances[i,j] = norm(coors_array[i,:] - coors_array[j,:])
         distances[j,i] = distances[i,j]
   end_time = time()
   file = open('/Users/cchang/Desktop/distance_matrix.npy', 'w')
   numpy.save(file, distances)
   file.close()
print 'Done' 

bond_threshold = 1.5  # Angstrom distance; if greater, then not bonded
# Need to create molecular groups of atom indices. Create as list of index lists.
#   Walk through distance matrix, starting with first atom, and crossing off atoms
#   from a master list as we go until empty.
index_array = list(numpy.arange(numatoms))
molecules = []
while len(index_array) > 0:
  first_atom = [index_array[0]]
  # Create list of atom indices; index from 1
  this_molecule = get_molecule(first_atom, bond_threshold)
  molecules.append(this_molecule)
  # Update index_array
  for i in this_molecule:
     index_array.remove(i)
atoms_in_fullmol = 0
for i in molecules:
   if len(i) > atoms_in_fullmol: atoms_in_fullmol = len(i)
for i in range(len(molecules)-1, -1, -1):
   if len(molecules[i]) < atoms_in_fullmol: molecules.pop(i)
# Test
#t = []
#for i in molecules:
#   print str(len(i)) + ' ',
#   for j in xrange(len(i)):
#      t.append(i[j])
#print
#t2 = [atoms[i] for i in t]
#testdump('testfull.xyz', atoms_in_fullmol*len(molecules), t2)

# Molecules should now have all complete and partial molecules in crystal chunk.
# Calculate centroids of each molecule, then centroid of all molecules.
# Don't worry about mass weighting yet.
centroids = numpy.zeros( (len(molecules), 3), numpy.float )
j = 0
for i in molecules:
   centroid = numpy.zeros( (1, 3), numpy.float )
   for atom_index in i:
      centroid += atoms[atom_index-1].get_coors()
   centroid /= len(i)
   centroids[j,:] = centroid
   j += 1

# Which is the molecule closest to center?
centroid_of_centroids = numpy.mean( centroids, axis=0 )
centroid_distances = numpy.zeros( (numpy.shape(centroids)[0]) )
for i in xrange(numpy.shape(centroids)[0]):
   centroid_distances[i] = numpy.linalg.norm(centroids[i,:] - centroid_of_centroids)
center_molecule_index = numpy.argmin(centroid_distances)

# Find out how many shells to take from user. Repurpose centroid_distances
#   to be distances from the center centroid, rather than from centroid of centroids.
numshells = int(raw_input('How many shells of molecules to take? '))
center = centroids[center_molecule_index, :]
for i in xrange(numpy.shape(centroids)[0]):
   centroid_distances[i] = numpy.linalg.norm(centroids[i,:] - center)
#print centroid_distances
centroid_max = numpy.amax(centroid_distances)
#print centroid_max

# Now test-cluster distances to find total number of shells.
from scipy.cluster.vq import kmeans
# For reasoning behind the following, see notebook 072815
kmeans_threshold = math.pow(500./numatoms, 1./3.)
#print kmeans_threshold

distortions = []
# Cluster with varying number of target clusters up to number of molecules.
#   Don't bother with full number of centroids, trivial one cluster per item.
#   (Python range loop stops at upper limit - 1)
for i in range(1,len(centroid_distances)):
   kmeans_initguess = numpy.array( [ j*centroid_max/i for j in range(1,i+1) ] )
   t = kmeans(centroid_distances, kmeans_initguess)
   distortions.append(t[1])
# Define number of shells as one more than the lowest number of clusters for which
#   distortion is below threshold. Adjust kmeans_threshold to taste.
for i in range(1,len(distortions)):
   if (distortions[i-1] - distortions[i]) < kmeans_threshold:
      k = i+1
      break

# k-means is not deterministic unless we pass guess centroids explicitly.
# Once know k, divide distances into k ranked (by distance) equally sized bins,
# and take borders of bins (not 0, which will be the centroid molecule itself)
# as the guesses.
kmeans_initguess = numpy.array( [ i*centroid_max/k for i in range(1,k+1) ] )
#print kmeans_initguess
clusters = kmeans(centroid_distances, kmeans_initguess)[0]
#print clusters

# Take all molecules with centroids within kmeans_threshold of clusters[numshells]
cutoff = clusters[numshells-1] + kmeans_threshold
mol_atom_groups = []
for i in centroid_distances:
   if i <= cutoff:
      mol_atom_groups.append(molecules[list(centroid_distances).index(i)])
atoms_out = []
for i in mol_atom_groups:
   for atom_index in i:
      atoms_out.append(atoms[atom_index])

# Test dump xyz of selection
for i in atoms_out:
   testdump('testdump.xyz', len(atoms_out), atoms_out)
#for j in moelcules:
#   testlist = [atoms[i] for i in j]
#   testdump('testdump' + str(molecules.index(j)) + '.xyz', len(testlist), testlist)
#print 'Time to build distance matrix was '
#print end_time - start_time
sys.exit()


# Common Q-Chem input
string1 = "$molecule\n0 1\n"

outfile = open(sys.argv[1][:-4] + '.qc', 'w')
geom_string = ''
for i in mol1_indices:
   geom_string += '%5s' % atoms[i].get_element()
   for j in atoms[i].get_coors():
      geom_string += '%12.6f' % j
   geom_string += '\n'
for i in mol2_indices:
   geom_string += '%5s' % atoms[i].get_element()
   for j in atoms[i].get_coors():
      geom_string += '%12.6f' % j
   geom_string += '\n'

#for i in mol1_indices:
#   outfile.write('%5s' % atoms[i].get_element())
#   for j in atoms[i].get_coors():
#      outfile.write('%12.6f' % j)
#   outfile.write('\n')
#for i in mol2_indices:
#   outfile.write('%5s' % atoms[i].get_element())
#   for j in atoms[i].get_coors():
#      outfile.write('%12.6f' % j)
#   outfile.write('\n')

string2 = '''$end

$rem
   mem_total  4000
   mem_static 2500
   basis  6-311G
   '''

string3 = '''
   fast_xc  true
   cis_n_roots  6
   cis_singlets  true
   cis_triplets  false
   rpa  true
   sts_fed  true
   sts_donor  1-30  True for all tetracene jobs with correct atom grouping
   sts_acceptor  31-60
$end

'''

separator_string = '\n@@@\n\n'
method_list = ['lda', 'bpw91', 'VSXC', 'b97', 'wB97X']
method_dict = {'lda': ('method  lda', 'LDA test'), \
   'bpw91': ('exchange  b88\n   correlation  pw91', 'GGA test'), \
   'VSXC': ('exchange  VSXC', 'meta-GGA test'), \
   'b97': ('exchange  b97', 'hybrid GGA test'), \
   'wB97X': ('method  wB97X', 'LRC-hybrid-GGA test')}
comment2_string=' on dimer structure in file ' + sys.argv[1] + '\n$end\n'

for i in method_list:
   if i != 'lda':
      outfile.write(separator_string)
   outfile.write(string1)
   outfile.write(geom_string)
   outfile.write(string2)
   outfile.write(method_dict[i][0])
   outfile.write(string3)
   outfile.write('$comment\n   ' + method_dict[i][1] + comment2_string)
outfile.close()

