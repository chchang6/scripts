#!/usr/bin/env python
# Matplotlib template to generate 2X2 grid of scatter plots.

import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0., 5., 0.2)

fig1 = plt.figure()
plot1 = fig1.add_subplot(2,2,1)
ser1a = plot1.plot(t, t)
ser1b = plot1.plot(t, t**0.75)
plt.setp(ser1a, color='r', marker='s')
plt.setp(ser1b, color='g', marker='s')
plot1.set_title('Example 1')
plot1.set_xlabel('Time')
plot1.set_ylabel('Stuff')
plot1.legend((ser1a, ser1b), ('t', r't$^\frac{3}{4}$'), loc='lower right')

plot2 = fig1.add_subplot(2,2,2)
ser2 = plot2.plot(t, t**0.5)
plt.setp(ser2, color='black', marker='s')
plot2.set_title('Example 2')
xaxislabel2 = plot2.set_xlabel('Time2')
yaxislabel2 = plot2.set_ylabel('sqrt(t)')

plot3 = fig1.add_subplot(2,2,3)
ser3 = plot3.plot(t, t**2)
plt.setp(ser3, color='b', marker='s')
xaxislabel3 = plot3.set_xlabel('Time')
yaxislabel3 = plot3.set_ylabel('t^2')

plot4 = fig1.add_subplot(2,2,4)
ser4 = plot4.plot(t, t**3)
plt.setp(ser4, color='g', marker='^')
xaxislabel4 = plot4.set_xlabel('Time')
yaxislabel4 = plot4.set_ylabel(r't$^3$')

fig1.savefig('test.png')
