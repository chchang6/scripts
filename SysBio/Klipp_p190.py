#!/usr/bin/env python
#  Script to calculate quantities in example 5-27 of Klipp et al., Systems Biology in Practice.
#   Weinheim: Wiley-VCH, 2005. ISBN 978-3-527-31078-4 

import numpy
import math

P0 = 1.
S1_init = 1.
S2_init = 1.
S3_init = 1.
P4 = 1.

enzymes = numpy.ones((4), numpy.float)
forward_rates = 2*numpy.ones((4), numpy.float)
backward_rates = numpy.ones((4), numpy.float)
substrates = numpy.array([P0, S1_init, S2_init, S3_init])
products = numpy.array([S1_init, S2_init, S3_init, P4])
enzymes[0] = 2.0
step = 0.1
stop = 1e-6
dS1_step = 0.; dS2_step = 0.; dS3_step = 0. # Initialize
while True:
   velocities = enzymes * (forward_rates*substrates - backward_rates*products)
   dS1_old = dS1_step
   dS2_old = dS2_step
   dS3_old = dS3_step
   dS1 = velocities[0] - velocities[1]; dS1_step = step*dS1
   dS2 = velocities[1] - velocities[2]; dS2_step = step*dS2
   dS3 = velocities[2] - velocities[3]; dS3_step = step*dS3
   if abs(dS1) < stop and abs(dS2) < stop and abs(dS3) < stop: break
   elif (dS1_step * dS1_old < 0.) and (dS2_step * dS2_old < 0.) and (dS3_step * dS3_old < 0.):
      print str(substrates[1]) + '\t' + str(dS1) + '\t' + str(substrates[2]) + '\t' + str(dS2) + '\t' + str(substrates[3]) + '\t' + str(dS3)
      step = step * 0.1
   else:
      print str(substrates[1]) + '\t' + str(dS1) + '\t' + str(substrates[2]) + '\t' + str(dS2) + '\t' + str(substrates[3]) + '\t' + str(dS3)
      substrates = substrates + numpy.array([0., dS1_step, dS2_step, dS3_step])
      products = products + numpy.array([dS1_step, dS2_step, dS3_step, 0.])

I_array = numpy.identity(4, numpy.float)
dgJ_array = numpy.identity(4, numpy.float)

I = numpy.asmatrix(I_array)
dgJ = numpy.asmatrix(dgJ_array)
N = numpy.asmatrix(numpy.array([[1,-1,0,0],[0,1,-1,0],[0,0,1,-1]], numpy.float))
dvdS = numpy.asmatrix(numpy.array([[2,0,0],[-1,2,0],[0,-1,2],[0,0,-1]], numpy.float))

result = I - dgJ.I * (dvdS * (N*dvdS).I * N) * dgJ
print result
