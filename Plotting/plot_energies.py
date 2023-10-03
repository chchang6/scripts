#!/usr/bin/env python
# Plot energy levels for various states relative to ground state

import re
import matplotlib.pyplot as plt
from matplotlib import lines

RE1 = re.compile('SP of (.+) @ ([^\t]{2,4})')
RE2 = re.compile('E = ([-\.0-9]+)')
RE3 = re.compile('E = S0 \+ ([\.0-9]+) eV')

eV_per_Ha = 27.211385

file = open('notes', 'r')
data = file.readlines()
file.close()

energies = {}

for i in data:
   t = RE1.search(i)
   if t:
      electronic_state = t.group(1)
      geometry = t.group(2)
      if RE3.search(i):   # Excited state
         E = float(RE3.search(i).group(1))
      else:
         E = float(RE2.search(i).group(1))
      energies[(electronic_state, geometry)] = E

ground_state_E = energies[('S0', 'S0')]

for i in energies:
   if energies[i] < 0.:
      new_E = (energies[i] - ground_state_E) * eV_per_Ha
      energies[i] = new_E

state_key = {'S0':1., 'S0-':2., 'S0+':3., 'T1':4., 'S1':5.}
color_key = {'S0':'k', 'S0-':'r', 'S0+':'b', 'T1':'g', 'S1':'c'}
figure = plt.figure()
axes = figure.add_subplot(1,1,1)
xlabel = axes.set_xlabel('State')
ylabel = axes.set_ylabel('Relative Energy (eV)')
axes.set_xlim(right=6)
axes.set_ylim(-2., 7.)
legend_lines = []
for i in energies:
   energy_line = lines.Line2D( (state_key[i[1]]-0.35, state_key[i[1]]+0.35), (energies[i], energies[i]), color=color_key[i[0]], lw=1)
   axes.add_line( energy_line )
   # Make legend from S0 geometry energies
   if i[1] == 'S0':
      #print energy_line.get_color()
      legend_lines.append( (i[0], energy_line) )
axes.set_xticklabels( ['', '$S_0$', '$S_0^-$', '$S_0^+$', '$T_1$', '$S_1$'] )

# Add legend in order of tick labels
legend_lines = sorted(legend_lines, key=lambda state: state_key[state[0]])
axes.legend( [i[1] for i in legend_lines], [i[0] for i in legend_lines], loc='center right', bbox_to_anchor=(1.0,0.6))

plt.savefig('state_energies.png')

