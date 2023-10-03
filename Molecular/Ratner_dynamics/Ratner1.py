#!/usr/bin/env python
# Implementing Ratner method.
# Base time unit fs, energy unit eV

import numpy as np
import pickle
from re import match as REmatch
from time import time

# Following value from http://en.wikipedia.org/wiki/Planck_constant, 11/8/11
hbar = 6.58211928e-01  # eV \cdot fs
timestep = 0.1  # In fs
time_to_integrate = 100  # In fs

# Parameters here are in eV
E_S1S0 = 0.0     # Energy of excited singlet
E_AC = 0.0       # Energy of anion @ "left"
E_CA = 0.0       # Energy of anion @ "right"
E_TT = 0.0       # Energy of dual-triplet states
T_H = 0.027      # Coupling of HOMOs for horizontal ET
T_L = 0.027      # Coupling of LUMOs for horizontal ET
T_D1 = 0.027     # Coupling of dual-triplet and ET state for right-to-left exc.
T_D2 = 0.027     # Coupling of dual-triplet and ET state for left-to-right exc.
K_L = 0.00027    # Dissipation of singlet on left chromophore
K_R = 0.00027    # Dissipation of singlet from right chromophore
K_TT = 0.00027   # Dissipation of dual-triplet other than SF

# Set up test job as described for Table 3, row 1
# Set up H0
H_0 = np.zeros((10,10), float)
# Set diagonal elements to energies
for i in range(10):
   if i >= 0 and i < 4:
      H_0[i,i] = E_S1S0
   elif i == 4 or i == 7:
      H_0[i,i] = E_AC
   elif i == 5 or i == 6:
      H_0[i,i] = E_CA
   else:
      H_0[i,i] = E_TT
rows = [i for i in range(8)]
cols = [4, 5, 6, 7, 0, 1, 2, 3]
for i in zip(rows,cols):
   H_0[i[0], i[1]] = T_H
cols = [5, 4, 7, 6, 1, 0, 3, 2]
for i in zip(rows,cols):
   H_0[i[0], i[1]] = T_L
rows = [5, 6, 8, 9]
cols = [8, 9, 5, 6]
for i in zip(rows,cols):
   H_0[i[0], i[1]] = T_D1
rows = [4, 7, 8, 9]
cols = [9, 8, 7, 4]
for i in zip(rows,cols):
   H_0[i[0], i[1]] = T_D2
#print H_0

# Set up Hd
H_d = np.zeros((10,10), np.cfloat)
H_d[0,0] = complex(0.0,-1.0)*K_L
H_d[1,1] = complex(0.0,-1.0)*K_R
H_d[2,2] = complex(0.0,-1.0)*K_R
H_d[3,3] = complex(0.0,-1.0)*K_L
H_d[8,8] = complex(0.0,-1.0)*K_TT
H_d[9,9] = complex(0.0,-1.0)*K_TT
#print(H_d)

# Set up initial density matrix. Assume diagonal entries are just normalized
#   populations; as in paper, populate S1 states equally.
rho = np.zeros((10,10), float)
for i in range(4):
   rho[i,i] = 0.25

# Set up arrays to collect population data. See Figure 4.
simtime = []
S1 = []
CT = []
TT = []
Fiss = [0.0]
Fluor = [0.0]

# For now, just do the following a fixed number of times.
for i in range(int(time_to_integrate/timestep)):
# Update data arrays
   simtime.append(i)
   S1.append(rho[0,0].real + rho[1,1].real + rho[2,2].real + rho[3,3].real)
   CT.append(rho[4,4].real + rho[5,5].real + rho[6,6].real + rho[7,7].real)
   TT.append(rho[8,8].real + rho[9,9].real)
   if i > 0:
      Fiss.append(timestep*(ihHdrho_anticomm[8,8].real + ihHdrho_anticomm[9,9].real))
      Fluor.append(timestep*(ihHdrho_anticomm[0,0].real + ihHdrho_anticomm[1,1].real + ihHdrho_anticomm[2,2].real + ihHdrho_anticomm[3,3].real))
# Calculate commutator of H0 and rho
   H0_times_rho = np.asmatrix(H_0)*np.asmatrix(rho)
   rho_times_H0 = np.asmatrix(rho)*np.asmatrix(H_0)
   H0rho_commutator = H0_times_rho - rho_times_H0
   # Calculate contribution to drhodt separately
   ihH0rho_commutator = complex(0.0,-1.0)*np.asarray(H0rho_commutator)/hbar
   #print ihH0rho_commutator
# Calculate anticommutator of H_d and rho
   Hd_times_rho = np.asmatrix(H_d)*np.asmatrix(rho, np.cfloat)
   rho_times_Hd = np.asmatrix(rho, np.cfloat)*np.asmatrix(H_d)
   Hdrho_anticomm = Hd_times_rho + rho_times_Hd
   # Calculate contribution to drhodt separately
   ihHdrho_anticomm = complex(0.0,-1.0)*np.asarray(Hdrho_anticomm)/hbar
   #print Hdrho_anticomm
# Calculate drho/dt. If base time unit != fs, add a "scale" multiplier
   drhodt = ihH0rho_commutator + ihHdrho_anticomm
   #print drhodt
# Change rho
   rho = rho + timestep*drhodt

data_file_name = REmatch('[0-9]+', str(time())).group(0) + '.pickle'
with open(data_file_name, 'wb') as data_file:
   pickle.dump(simtime, data_file)
   pickle.dump(S1, data_file)
   pickle.dump(CT, data_file)
   pickle.dump(TT, data_file)
   pickle.dump(Fiss, data_file)
   pickle.dump(Fluor, data_file)
