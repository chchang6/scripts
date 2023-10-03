#!/usr/bin/env python
from pylab import *
from scipy import optimize
import numpy
import sys

datafile = open(sys.argv[1], 'r')
data = datafile.readlines()
datafile.close()
xdata = []
ydata = []
for i in data:
   line = i.split()
   xdata.append(line[0])
   ydata.append(line[1])
xdata = numpy.array(xdata)
ydata = numpy.array(ydata)

linfitfunc = lambda p,x: p[0]*x + p[1]
linerrfunc = lambda p,x,y: linfitfunc(p,x) - y
expfitfunc = lambda p,x: p[0]*(1 - exp(p[1]*x))
experrfunc = lambda p,x,y: errfitfunc(p,x) - y

# Initial guesses
lin_p = [4,0.1]
exp_p = [1,1]

# Fit to linear
lin_p_out, success1 = optimize.leastsq(linerrfunc, lin_p, args=(xdata, ydata))
# Fit to exponential
exp_p_out, success2 = optimize.leastsq(experrfunc, exp_p, args=(xdata, ydata))

# Create x array for curves
x_fit = linspace(xdata.min(), xdata.max(), 100)

# Plot
plot(xdata, ydata, "ro", x_fit, linfitfunc(lin_p, x_fit), "b-", x_fit, expfitfunc(exp_p_out, x_fit), "k-")

# Legend
title("Linear vs. exponential fit of ...")
xlabel("x")
ylabel("y")
legend(('data', 'linear fit', 'exponential fit'))

ax = axes()

text(0.8, 0.07,
     'Linear: m = %.3f b = %.3f \n Exponential: k1 = %.3f k2 = %.3f' % (lin_p_out[0], lin_p_out[1], exp_p_out[0], exp_p_out[1]),
      horizontalalignment = 'right',
      verticalalignment = 'center',
      transform=ax.transAxes)

#text(0.8, 0.07,
#     'x freq :  %.3f kHz \n y freq :  %.3f kHz' % (1/p1[1],1/p2[1]),
#     fontsize=16,
#     horizontalalignment='center',
#     verticalalignment='center',
#     transform=ax.transAxes)

show()

