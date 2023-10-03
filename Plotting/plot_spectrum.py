#!/usr/bin/env python
# Script to parse a file with N consecutive ZINDO calculations, and plot spectrum
# for each.

import re, sys
import numpy
import matplotlib.pyplot as plt

RE1 = re.compile(' Convergence achieved on expansion vectors')
RE2 = re.compile(' Ground to excited state transition velocity dipole moments')
RE3 = re.compile(' Convergence on energies')

Gauss_broadening = 1e-4
num_x_points = 300
numroots = 0
spectrum_index = 1
spectra = {}
file = open(sys.argv[1], 'r')
data = list('a'*20)  # Keep up to 20 lines as file gets read, allows backtracking
                     # through up to 20 roots.
got_osc = False
while True:
   t = file.readline()
   if t == '': break
   else: data.append(t)
   if RE1.match(t) or RE3.match(t):
      if numroots == 0:
         numroots = int(data[-2].split()[1])
      energies = []
      for i in xrange(numroots):
         energies.append(float(data[-2 - i].split()[3]))
   elif RE2.match(t):
      osc_strengths = []
      for i in xrange(numroots):
         osc_strengths.append(float(data[-2 - i].split()[4]))
      got_osc = True
   if got_osc == True:
      got_osc = False
      energies.reverse(); osc_strengths.reverse()
      spectra[spectrum_index] = (energies, osc_strengths)
      spectrum_index += 1
   data.pop(0)
file.close()

# Get spectral energy range in eV
E_min = 1000.
E_max = 0.
for i in spectra:
   for j in spectra[i][0]:
      if j < 0.: continue
      if j < E_min: E_min = j
      if j > E_max: E_max = j

# Create list of spectra to plot
baseline = numpy.zeros((num_x_points), numpy.float)
x = numpy.arange(0.9*E_min, 1.1*E_max, (1.1*E_max - 0.9*E_min)/float(num_x_points))
plot_spectrum_list = []
max_spectrum_intensity = 0.
for i in range(1, len(spectra)+1):
   spectrum = baseline
   for j in xrange(numroots):
      E = spectra[i][0][j]
      OS = spectra[i][1][j]
      spectrum = spectrum + OS*numpy.exp(-1. * numpy.square(x - E) / (2*Gauss_broadening))
   if numpy.max(spectrum) > max_spectrum_intensity: max_spectrum_intensity = numpy.max(spectrum)
for i in range(1, len(spectra)+1):
   spectrum = baseline
   for j in xrange(numroots):
      E = spectra[i][0][j]
      OS = spectra[i][1][j]
      spectrum = spectrum + OS*numpy.exp(-1. * numpy.square(x - E) / (2*Gauss_broadening))
   plot_spectrum_list.append(spectrum + (i-1)*max_spectrum_intensity)

fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
plot1.set_title('Porphine stretch spectra')
plot1.set_xlabel('Energy (eV)')
plot1.set_ylabel('Intensity')
colors = ['k', 'r', 'b', 'g']
for i in xrange(len(spectra)):
   # Following just a diagnostic report
   print spectra[i+1][0][0]
   # This generates the plot
   ser = plot1.plot(x, plot_spectrum_list[i])
   plt.setp(ser, color=colors[i%len(colors)], marker=None, linewidth=1)
fig1.savefig('spectra.png')

