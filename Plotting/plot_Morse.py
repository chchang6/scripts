#!/usr/bin/env python
# Script to plot out three Morse potentials and their force curves

import math
import numpy as np
import matplotlib.pyplot as plt

# Morse potential has the form V(x) = D_e(1-exp(-a*(x-x_ref))^2
# Morse potential force constant k_e is 2 * a^2* D_e
#   a is the exponential constant
# dV/dx = 2 * D_e * (1 - exp(-a*(x-x_ref))) * (a*exp(-a* (x-x_ref)))

k_1 = 10.
k_2 = 3 * k_1
k_3 = 9 * k_1
D_e = 50.
x_ref = 2.0
a_1 = math.sqrt(k_1 / (2.*D_e))
a_2 = math.sqrt(k_2 / (2.*D_e))
a_3 = math.sqrt(k_3 / (2.*D_e))
x = np.arange(0, 15, 0.01, np.float)
y_1 = D_e * np.square( np.ones_like(x) -  np.exp( -a_1*(x - x_ref) ) )
dy_1dx = 2 * D_e * np.multiply( ( np.ones_like(x) -  np.exp( -a_1*(x - x_ref) ) ), a_1*np.exp(-a_1*(x - x_ref)))
y_2 = D_e * np.square( np.ones_like(x) -  np.exp( -a_2*(x - x_ref) ) )
dy_2dx = 2 * D_e * np.multiply( ( np.ones_like(x) -  np.exp( -a_2*(x - x_ref) ) ), a_2*np.exp(-a_2*(x - x_ref)))
y_3 = D_e * np.square( np.ones_like(x) -  np.exp( -a_3*(x - x_ref) ) )
dy_3dx = 2 * D_e * np.multiply( ( np.ones_like(x) -  np.exp( -a_3*(x - x_ref) ) ), a_3*np.exp(-a_3*(x - x_ref)))

fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
plot1.set_title('Morse potentials')
plot1.set_xlabel('Displacement')
plot1.set_ylabel('Energy or Force')
plot1.set_ylim(-10,50)
ser1 = plot1.plot(x, y_1)
ser1b = plot1.plot(x, dy_1dx)
plt.setp(ser1, color='k', marker=None, linewidth=1)
plt.setp(ser1b, color='k', marker=None, linewidth=1)
ser2 = plot1.plot(x, y_2)
ser2b = plot1.plot(x, dy_2dx)
plt.setp(ser2, color='r', marker=None, linewidth=1)
plt.setp(ser2b, color='r', marker=None, linewidth=1)
ser3 = plot1.plot(x, y_3)
ser3b = plot1.plot(x, dy_3dx)
plt.setp(ser3, color='b', marker=None, linewidth=1)
plt.setp(ser3b, color='b', marker=None, linewidth=1)
fig1.savefig('Morse.png')

