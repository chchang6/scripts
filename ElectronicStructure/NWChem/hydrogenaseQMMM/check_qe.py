#!/usr/bin/env python
# Script to take NWChem geom block as input in separate file,
#   calculate what the number of electrons and overall charge should be
#   with Bq's counted. NWChem requires overall charge to be set to what this charge should be, PLUS
#   the difference between the sum of Bq charges and this overall charge.

file = open('temp', 'r')
data = file.readlines()
file.close()

Bq_charge = 0
charge = 0
num_electrons = 0
elec_dict = { 'H': 1, \
              'C': 6, \
              'N': 7, \
              'O': 8, \
              'S': 16}

for i in data:
   temp = i.split()
   if temp[-2] == 'charge' and temp[0] == 'Bq':
      Bq_charge += int(float(temp[-1]))
      charge += int(float(temp[-1]))
   elif temp[-2] == 'charge' and temp[0] != 'Bq':
      num_electrons += elec_dict[temp[0][0]] + (elec_dict[temp[0][0]] - int(float(temp[-1])))
      charge += (int(float(temp[-1])) - elec_dict[temp[0][0]])
   else:
      num_electrons += elec_dict[temp[0][0]]

print 'Overall charge of system is ' + str(charge)
print 'Number of electrons is ' + str(num_electrons)
print 'Set overall charge in NWChem to ' + str(2*charge - Bq_charge)
