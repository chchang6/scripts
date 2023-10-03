#!/usr/bin/env python
# Plot of binding energy for butylamine on 4X4X4 Ag grid.

import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit
from scipy import interpolate

approximate_dissociation = 165. # Shift to bring curve into 0 range
font = 'Arial'

#def Morse(x,De,a,re,c):
#   # V = De(1-exp(-a(r-re)))^2
#   # x is the independent variable data array
#   return De * np.power( (1 - np.exp(-a * (x-re))), 2*np.ones((1,len(x))).flatten() ) + c

d = np.arange(-1.0, 5.5, 0.5)  # Distance of N displacement from optimum along z (normal to Ag surface)
eV = np.array([-164.782028, -165.386490, -165.568573, -165.437357, -165.285269, -165.213369, -165.181319, \
               -165.165303, -165.156913, -165.152158, -165.149606, -165.148138, -165.146857]).flatten()

kcal = (eV + np.ones((1,len(eV))).flatten()*approximate_dissociation) * 23.0609

#popt, pcov = curve_fit(Morse, d, kcal)
#kcal = kcal - popt[0] - np.ones((1,13)).flatten()*popt[3]
#xfit = np.arange(-1.0, 5.5, 0.01)
#yfit = Morse(xfit, 10., 1.1, 0, -1*popt[0])

spline_rep = interpolate.splrep(d, kcal)
xspline = np.arange(-1.5, 6.0, 0.05)
yspline = interpolate.splev(xspline, spline_rep)

fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
plot1.set_xlim(left = -1.4, right = 6., auto = False)
plot1.set_ylim(bottom = -15., top = 30., auto = False)
ser1a = plot1.plot(d, kcal)
ser1b = plot1.plot(xspline, yspline)
plt.setp(ser1a, color='k', marker='s', linewidth=0)
plt.setp(ser1b, color='k', marker='.', markersize=0)
title = plot1.set_title('Butylamine binding energy to Ag(100)')
xlabel = plot1.set_xlabel(r'N z displacement from optimum ($\AA$)')
ylabel = plot1.set_ylabel('Energy (kcal/mol)')
label1 = plot1.text(3, 15, '$\Delta G_{bind}$ = -10 kcal/mol')

# Set fonts
title.set_fontname(font)
xlabel.set_fontname(font)
ylabel.set_fontname(font)
label1.set_fontname(font)
for i in plot1.xaxis.get_major_ticks():
   i.label1.set_fontname(font)
for i in plot1.yaxis.get_major_ticks():
   i.label1.set_fontname(font)

fig1.savefig('test.pdf', format='pdf')
