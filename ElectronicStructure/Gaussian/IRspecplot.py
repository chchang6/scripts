#!/usr/bin/env python

import re
import numpy
import matplotlib.pyplot as plt

def Gaussian(scale, freq, inten):
   sigma2 = 20.0
   x = numpy.arange(2000, 3500, 1)
   y = inten * numpy.exp( -1. * numpy.square(x-scale*freq)/(2*sigma2) )
   return y

RE1 = re.compile('Frequencies')
RE2 = re.compile('IR Inten')
freq_scale = 0.9512  # From JCPA 111: 11683 (2007) for 6-31G(d)

file = open('GmvhoUskEw7', 'r')
data = file.readlines()
file.close()

frequencies = []
intensities = []

for i in xrange(len(data)):
   if RE1.search(data[i]):
      t = data[i].split()
      for j in t:
         try:
            f = float(j)
            frequencies.append(f)
         except ValueError:
            continue
   elif RE2.search(data[i]):
      t = data[i].split()
      for j in t:
         try:
            intensity = float(j)
            intensities.append(intensity)
         except ValueError:
            continue
# Create array of Gaussian functions. Each row is a Gaussian; each column is a wavenumber point.
data = numpy.zeros( (len(frequencies), 1500), numpy.float)  # 1500 = 3500 - 2000, bounds of spectrum
counter = 0
for (i,j) in zip(frequencies, intensities):
   data[counter, :] = Gaussian(freq_scale,i,j)
   counter += 1
spectrum = numpy.sum(data,0)

# Plot
fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
x = numpy.arange(2000, 3500, 1)
ser1a = plot1.plot(x, spectrum)
plt.setp(ser1a, color='k', marker=None, linewidth=1)
plot1.set_xlabel(r'Frequency ($cm^{-1}$)')
plot1.set_xlim(left = 2000, right = 3400, auto = False)
plot1.set_ylim(bottom = -1.0, top = 1500., auto = False)
plot1.tick_params(axis='x', width=1, bottom='on', top='off')
plot1.tick_params(axis='y', left='off', right='off')
plot1.set_yticklabels([str(i) for i in xrange(10)], visible=False)
plot1.set_frame_on(False)
fig1.savefig('test.pdf')
