#!/usr/bin/env python
file = open('CpI_OO_O_OOR_QMMM-active.pdb', 'r')
data = file.readlines()
file.close()
x = []
y = []
z = []
for i in data:
   temp = i.strip().split()
   x.append(float(temp[3]))
   y.append(float(temp[4]))
   z.append(float(temp[5]))
print 'Minimum and maximum x: ' + str(min(x)) + ' and ' + str(max(x))
print 'Minimum and maximum y: ' + str(min(y)) + ' and ' + str(max(y))
print 'Minimum and maximum z: ' + str(min(z)) + ' and ' + str(max(z))
