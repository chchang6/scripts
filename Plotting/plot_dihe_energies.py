#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

file = open('GjuyUU_4.results', 'r')
data = file.readlines()
file.close()

# Parse and store
data_dict = {}
raw_energies = []
for i in data:
   if i[0:4] == '  C3':
      t1 = i.rstrip().split()[-1]
      t1 = int(t1[2:-1])  # Strip of parentheses and sign
      key = t1
   elif i[0:4] == ' SCF':
      t2 = float(i.split()[4])   
      data_dict[key] = t2
      raw_energies.append(t2)
E_max = max(raw_energies)
for i in data_dict:
   data_dict[i] = (data_dict[i] - E_max) * 627.51

x = data_dict.keys()
x.sort()
y = []
for i in x:
   y.append(data_dict[i])
fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
ser1a = plot1.plot(np.array(x), np.array(y))
plt.setp(ser1a, color='k', marker='s')
plot1.set_title('Energy vs. Allyl $\pi$ / Co-C7 dihedral angle')
plot1.set_xlabel('Dihedral angle (degrees) vs. optimum')
plot1.set_ylabel('Energy vs. maximum (kcal/mol)')
fig1.savefig('GjuyUU_4.png')
