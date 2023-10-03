#!/usr/bin/env python
# Used to remove dihedrals involving near-linear angles.
file = open('HCO.sgm', 'r')
data = file.readlines()
file.close()
numbers_of_things = data[3].split()
number_of_atoms = int(numbers_of_things[0])
number_of_bonds = int(numbers_of_things[1])
number_of_angles = int(numbers_of_things[2])
number_of_dihedrals = int(numbers_of_things[3])
dihedral_start = 2*(number_of_atoms + number_of_bonds + number_of_angles) + 5
i = dihedral_start
while i:
   test = data[i].split()
   for j in [1,2]:
       if (test[j] == '1' and (test[j+1] == '10' and test[j+2] == '5') or \
           (test[j+1] == '11' and test[j+2] == '6')) or \
          (test[j+2] == '1' and (test[j+1] == '10' and test[j] == '5') or \
           (test[j+1] == '11' and test[j] == '6')) or \
          (test[j] == '2' and (test[j+1] == '13' and test[j+2] == '8') or \
           (test[j+1] == '14' and test[j+2] == '9')) or \
          (test[j+2] == '2' and (test[j+1] == '13' and test[j] == '8') or \
           (test[j+1] == '14' and test[j] == '9')) or \
          (test[j] == '3' and (test[j+1] == '1' and test[j+2] == '10') or \
           (test[j+1] == '2' and test[j+2] == '13')) or \
          (test[j+2] == '3' and (test[j+1] == '1' and test[j] == '10') or \
           (test[j+1] == '2' and test[j] == '13')) or \
          (test[j] == '4' and (test[j+1] == '1' and test[j+2] == '11') or \
           (test[j+1] == '2' and test[j+2] == '14')) or \
          (test[j+2] == '4' and (test[j+1] == '1' and test[j] == '11') or \
           (test[j+1] == '2' and test[j] == '14')):
          del data[i:i+2]
          number_of_dihedrals -= 1
          i -= 2
   if test[0] == '1' and i > dihedral_start:
      i = 0
   else:
      i += 2
# Now change dihedral indices
for i in range(0, 2*number_of_dihedrals, 2):
   temp = data[i+dihedral_start].split()
   temp[0] = (i+2)/2
   for j in xrange(len(temp)):
      temp[j] = int(temp[j])
   data[i+dihedral_start] = '%5i%5i%5i%5i%5i%5i%5i\n' % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6])
fileout = open('test', 'w')
for i in xrange(len(data)):
   if i == 3:
      temp = data[i].strip().split()
      temp[3] = number_of_dihedrals
      for j in xrange(len(temp)):
         temp[j] = int(temp[j])
         fileout.write('%5i' % temp[j])
      fileout.write('\n')
   else:
      fileout.write(data[i])
fileout.close()
