#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

approximate_dissociation = 165. # Shift to bring curve into 0 range
font = 'Arial'

file = open('energies', 'r')
data = file.readlines()
file.close()

x = []  # C-C-Co angle deviation from transition state
y = []  # Energy relative to transition state

for i in range(1, len(data)):
   t = data[i].strip().split()
   x.append(int(float(t[0])))
   y.append(float(t[1]))
x.reverse(); y.reverse()
x = -1*np.array(x)
y = np.array(y)
# limits
xmin = min(x)
xmax = max(x)
ymin = min(y) - 1.0
ymax = max(y) + 1.0

spline_rep = interpolate.splrep(x, y)
xspline = np.arange(xmin, xmax, 0.05)
yspline = interpolate.splev(xspline, spline_rep)

fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
plot1.set_xlim(left = xmin, right = xmax, auto = False)
plot1.set_ylim(bottom = ymin, top = ymax, auto = False)
ser1a = plot1.plot(x, y)
ser1b = plot1.plot(xspline, yspline)
plt.setp(ser1a, color='k', marker='s', linewidth=0)
plt.setp(ser1b, color='k', marker='.', markersize=0)
title = plot1.set_title('Reverse C-C-Co angle scan from TS2_5')
xlabel = plot1.set_xlabel(r'Angle versus TS ($^{\circ}$)')
ylabel = plot1.set_ylabel('Energy relative to TS (kcal/mol)')

# Set fonts
title.set_fontname(font)
xlabel.set_fontname(font)
ylabel.set_fontname(font)
for i in plot1.xaxis.get_major_ticks():
   i.label1.set_fontname(font)
for i in plot1.yaxis.get_major_ticks():
   i.label1.set_fontname(font)

fig1.savefig('energies.pdf', format='pdf')
