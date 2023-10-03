#!/usr/bin/env python

import numpy
import matplotlib.pyplot as plt

file = open('results2.dat', 'r')
data = file.readlines()
file.close()

d = {}
keys = data[0].strip().split()
num_cpds = len(keys)/2
for i in keys:
   d[i] = []
for i in range(1,5):
   temp = data[i].strip().split()
   for j in xrange(len(keys)):
      d[keys[j]].append(float(temp[j]))

# Calculate percentage deviations of computed from experimental for each compound and each time point.
#   Store in new dictionary with compound name keys.
perc_dict = {}
for i in d:
   temp = []
   if i[-5:] == '_expt':
      prefix = i.rstrip('_expt')
      for j in xrange(len(d[i])):
         temp.append( 100*(d[i][j] - d[prefix+'_comp'][j]) / d[i][j] )
      perc_dict[prefix] = numpy.array(temp)

fig1 = plt.figure(figsize=(8, 10))
plot1 = fig1.add_axes([0.2, 0.5, 0.7, 0.4])
bar_width = 0.25
x = numpy.arange(0, 2*num_cpds, 2)
minor_x = numpy.concatenate((x+bar_width/2, x+1.5*bar_width, x+2.5*bar_width, x+3.5*bar_width))
minor_x = numpy.sort(minor_x)
keys = perc_dict.keys()
ser1a = plot1.bar(x, [perc_dict[i][0] for i in keys], bar_width, color='r', label='Start')
ser1b = plot1.bar(x+bar_width, [perc_dict[i][1] for i in keys], bar_width, color='y', label='1 hour')
ser1c = plot1.bar(x+2*bar_width, [perc_dict[i][2] for i in keys], bar_width, color='g', label='2 hours')
ser1d = plot1.bar(x+3*bar_width, [perc_dict[i][3] for i in keys], bar_width, color='b', label='4 hours')
plot1.set_title('Fitting Results, Dataset PG2')
plot1.set_xlabel('Compound')
plot1.set_ylabel('Percentage deviation from experiment')
#plot1.legend((ser1a, ser1b, ser1c, ser1d), ('Start', '1 hour', '2 hours', '4 hours'), loc='upper right')
plot1.set_xticks(x + 2*bar_width)
plot1.set_xticklabels(tuple(keys), rotation=45, ha='right', y=-0.1)
plot1.set_xticks(minor_x, minor=True)
plot1.set_xticklabels(len(keys)*['0','1','2','4'], minor=True)

fig1.savefig('test.png')
