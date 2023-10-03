#!/usr/bin/env python

import sys, re

def limits(list):
   min = list[0]
   max = list[0]
   for i in list:
      if i < min: min = i
      elif i > max: max = i
   return(min,max)

def get_geom(index):
   global data
   list = []
   i = index + 7
   while i:
      if RE4.match(data[i]): break
      else:
         list.append(data[i])
         i += 1
   return list

#RE1 = re.compile('^geometry')
#RE2 = re.compile('end')
RE3 = re.compile('Geometry')
RE4 = re.compile('^$')

file = open(sys.argv[1], 'r')
data = file.readlines()
file.close()
i = 0
while True:
   if RE3.search(data[i]):
      coord = get_geom(i)
      break
   else: i += 1

x = []; y = []; z = []
for i in coord:
   temp = i.strip().split()
   #x.append(float(temp[1]))
   #y.append(float(temp[2]))
   #z.append(float(temp[3]))
   x.append(float(temp[3]))
   y.append(float(temp[4]))
   z.append(float(temp[5]))
xrange = limits(x)
yrange = limits(y)
zrange = limits(z)
print 'x ranges from ' + str(xrange[0]) + ' to ' + str(xrange[1])
print 'y ranges from ' + str(yrange[0]) + ' to ' + str(yrange[1])
print 'z ranges from ' + str(zrange[0]) + ' to ' + str(zrange[1])
