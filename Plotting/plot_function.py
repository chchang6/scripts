#!/usr/bin/env python
# Script to plot specified function as scatter data. CHC 08/09/10
# 2/11/16: Changed to modularize function being plotted as def

import sys, math
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def Boltzmann(xrange):
   # Plot e^(E/kt) with xarray expressed as ratios in exponent, from xrange[0] to xrange[1]
   # Work with logarithmic x data
   xstart = math.log10(xrange[0])
   xstop = math.log10(xrange[1])
   numsteps = 100
   increment = (xstop-xstart)/numsteps
   xdata = [xstart]
   for i in range(100):
      xdata.append(xdata[-1] + increment)
   xarray = np.array(xdata)
   yarray = np.exp(-1 * 10**xarray)
   xlabel = r'$log_{10} (\frac{\delta E}{kT}$)'
   ylabel = r'$e^{\left( -10^x \right)}$'
   return (xarray, xlabel, yarray, ylabel)

(x_data, x_label, y_data, y_label) = Boltzmann((0.01, 10))
plt.plot(x_data, y_data)
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.show()
#plt.savefig('test.png')
