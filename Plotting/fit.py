#!/usr/bin/env python
# Script to do 2D least-squares fits and plot given discrete data. 06/30/10
#   Parsing is particular to Excel format with data series sequential, increasing number of intermediate tabs
#   in columns.

import sys, math
import numpy
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

def exp1((C, k, x0), x):
   return C*(1. - numpy.exp(-k * (x - x0)))

def exp1_residuals(parameter_tuple, ydata, xdata):
   C, k, x0 = parameter_tuple
   err = ydata - exp1(parameter_tuple, xdata)
   return err

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()

series1_x = numpy.zeros((0), numpy.float)
series2_x = numpy.zeros((0), numpy.float)
series3_x = numpy.zeros((0), numpy.float)
series4_x = numpy.zeros((0), numpy.float)
series1_y = numpy.zeros((0), numpy.float)
series2_y = numpy.zeros((0), numpy.float)
series3_y = numpy.zeros((0), numpy.float)
series4_y = numpy.zeros((0), numpy.float)

for i in data:
   temp = i.strip().split('\t')
   try:
      float(temp[0])
   except ValueError:
      headers = temp
      continue
   if len(temp) == 2: # First data series
      series1_x = numpy.append(series1_x, float(temp[0]))
      series1_y = numpy.append(series1_y, float(temp[1]))
   elif len(temp) == 3: # Second data series
      series2_x = numpy.append(series2_x, float(temp[0]))
      series2_y = numpy.append(series2_y, float(temp[2]))
   elif len(temp) == 4: # Third data series
      series3_x = numpy.append(series3_x, float(temp[0]))
      series3_y = numpy.append(series3_y, float(temp[3]))
   elif len(temp) == 5: # Fourth data series
      series4_x = numpy.append(series4_x, float(temp[0]))
      series4_y = numpy.append(series4_y, float(temp[4]))

p0 = [1., 1., 0.01]
plsq1 = leastsq(exp1_residuals, p0, args=(series1_y, series1_x))
plsq2 = leastsq(exp1_residuals, p0, args=(series2_y, series2_x))
plsq3 = leastsq(exp1_residuals, p0, args=(series3_y, series3_x))
plsq4 = leastsq(exp1_residuals, p0, args=(series4_y, series4_x))
stepsize = 50
fit_x1data = numpy.arange(numpy.amin(series1_x), numpy.amax(series1_x), (numpy.amax(series1_x) - numpy.amin(series1_x)) / stepsize)
fit_y1data = exp1(plsq1[0], fit_x1data)
fit_x2data = numpy.arange(numpy.amin(series2_x), numpy.amax(series2_x), (numpy.amax(series2_x) - numpy.amin(series2_x)) / stepsize)
fit_y2data = exp1(plsq2[0], fit_x2data)
fit_x3data = numpy.arange(numpy.amin(series3_x), numpy.amax(series3_x), (numpy.amax(series3_x) - numpy.amin(series3_x)) / stepsize)
fit_y3data = exp1(plsq3[0], fit_x3data)
fit_x4data = numpy.arange(numpy.amin(series4_x), numpy.amax(series4_x), (numpy.amax(series4_x) - numpy.amin(series4_x)) / stepsize)
fit_y4data = exp1(plsq4[0], fit_x4data)
plt.plot(series1_x, series1_y, 'o', fit_x1data, fit_y1data, series2_x, series2_y, 'v', fit_x2data, fit_y2data, \
         series3_x, series3_y, '^', fit_x3data, fit_y3data, series4_x, series4_y, '<', fit_x4data, fit_y4data)
#plt.show()
plt.savefig('test.png')
print plsq1[0]
print plsq2[0]
print plsq3[0]
print plsq4[0]
