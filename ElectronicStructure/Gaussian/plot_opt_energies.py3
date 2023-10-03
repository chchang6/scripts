#!/usr/bin/env python3

import sys, re
from numpy import array
#from matplotlib import use
#use('Agg')
import matplotlib.pyplot as plt 

RE1 = re.compile(' Step number {1,}(?P<step>[0-9]+)')
RE2 = re.compile(' SCF Done:  E\(UwB97X\) = {1,}(?P<energy>-[0-9]{1,}\.[0-9]{1,})')

file = open(sys.argv[1], 'r')
steps = []
energies = []
while True:
   t = file.readline()
   if RE1.match(t):
      step_number = RE1.match(t).group('step')
   t2 = RE2.match(t)
   if t2:
      try:
         steps.append(int(step_number))
         energies.append(float(t2.group('energy')))
         #print('Step %s energy %12.6f' % (step_number, float(t2.group('energy'))))
      except NameError:
         continue
   if len(t) == 0:
      file.close()
      break

for i in range(len(energies)):
   print('Step %3i Energy = %12.6f' % (steps[i], energies[i]))

plt.figure()
plt.plot(array(steps), array(energies))
plt.xlabel('Step Number')
plt.ylabel('Energy (Ha)')
plt.savefig('optimization.png')

