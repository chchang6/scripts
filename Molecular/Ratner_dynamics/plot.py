#!/usr/bin/env python
# Plot simulated singlet fission data from pickled data file produced by 
#   Ratner1.py. CHC 11/08/11.

import matplotlib.pyplot as plt
import numpy as np
import pickle, sys

data_file = open(sys.argv[1], 'rb')
simtime = np.asarray(pickle.load(data_file)) * 0.1 # Data is stored as timestep index, but each one is 0.1 fs.
#print len(simtime)
S1 = np.asarray(pickle.load(data_file))
#print len(S1)
CT = np.asarray(pickle.load(data_file))
#print len(CT)
TT = np.asarray(pickle.load(data_file))
#print len(TT)
Fiss = pickle.load(data_file)
#print np.where( Fiss > 0.0 )
Fluor = pickle.load(data_file)
print(np.sum(Fluor))
#print np.where( Fluor > 0.0 )
data_file.close()

# Calculate Yield array
CumFiss = -1.*np.cumsum(Fiss)
CumFluor = -1.*np.cumsum(Fluor)
Yield = []
for i in range(len(CumFiss)):
   if CumFiss[i] - 0.0 < 1e-50 and CumFluor[i] - 0.0 < 1e-50:  # Both are 0
      Yield.append(0.0)
   else:
      Yield.append(CumFiss[i]/(CumFiss[i]+CumFluor[i])) 
#print len(Yield)
fig1 = plt.figure()
plot1 = fig1.add_subplot(1,1,1)
ser1a = plot1.plot(simtime, S1)
ser1b = plot1.plot(simtime, CT)
ser1c = plot1.plot(simtime, TT)
ser1d = plot1.plot(simtime, CumFiss)
ser1e = plot1.plot(simtime, CumFluor)
ser1f = plot1.plot(simtime, Yield)
plt.setp(ser1a, color='b', linestyle='-')
plt.setp(ser1b, color='r', linestyle='-')
plt.setp(ser1c, color='g', linestyle='-')
plt.setp(ser1d, color='m', linestyle='--')
plt.setp(ser1e, color='y', linestyle='--')
plt.setp(ser1f, color='k', linestyle='-')
plot1.set_title('Example 1')
plot1.set_xlabel('Time (fs)')
plot1.set_ylabel('Population')
#plot1.legend((ser1a, ser1b), ('t', r't$^\frac{3}{4}$'), loc='lower right')
#
#plot2 = fig1.add_subplot(2,2,2)
#ser2 = plot2.plot(t, t**0.5)
#plt.setp(ser2, color='black', marker='s')
#plot2.set_title('Example 2')
#xaxislabel2 = plot2.set_xlabel('Time2')
#yaxislabel2 = plot2.set_ylabel('sqrt(t)')
#
#plot3 = fig1.add_subplot(2,2,3)
#ser3 = plot3.plot(t, t**2)
#plt.setp(ser3, color='b', marker='s')
#xaxislabel3 = plot3.set_xlabel('Time')
#yaxislabel3 = plot3.set_ylabel('t^2')
#
#plot4 = fig1.add_subplot(2,2,4)
#ser4 = plot4.plot(t, t**3)
#plt.setp(ser4, color='g', marker='^')
#xaxislabel4 = plot4.set_xlabel('Time')
#yaxislabel4 = plot4.set_ylabel(r't$^3$')
#
fig1.savefig('test.png')
