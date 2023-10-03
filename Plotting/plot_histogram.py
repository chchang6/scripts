#!/usr/bin/env python

import numpy
import matplotlib.pyplot as plt

eV_per_Ha = 27.211396641

file = open('energies.txt', 'r')
data = file.readlines()
file.close()

T1s = []
S1s = []

# Compute T1 and S1 relative energies
for i in range(1,len(data)):
   t = data[i].split()
   abs_S0 = float(t[1])
   abs_T1 = float(t[2])
   abs_S1 = float(t[3])
   T1s.append( (abs_T1 - abs_S0)*eV_per_Ha ) 
   S1s.append( (abs_S1 - abs_S0)*eV_per_Ha ) 

T1s = numpy.asarray(T1s)
T1_average = numpy.mean(T1s)
T1_SD = numpy.std(T1s)
S1s = numpy.asarray(S1s)
S1_average = numpy.mean(S1s)
S1_SD = numpy.std(S1s)

# Calculate and plot T1 histogram
n, bins, patches = plt.hist(T1s, 20, facecolor='red')
plt.title('T1 energy distribution over G09 functional')
plt.xlabel('T1 relative energy (eV)')
plt.ylabel('Number')
plt.text(1.1, 50, 'E = %6.3f $\pm$ %6.3f eV' % (T1_average, T1_SD))
plt.savefig('T1s.png')
plt.close()

# Calculate and plot S1 histogram
n, bins, patches = plt.hist(S1s, 20, facecolor='blue')
plt.title('S1 energy distribution over G09 functional')
plt.xlabel('S1 relative energy (eV)')
plt.ylabel('Number')
plt.text(2.0, 50, 'E = %6.3f $\pm$ %6.3f eV' % (S1_average, S1_SD))
plt.savefig('S1s.png')
