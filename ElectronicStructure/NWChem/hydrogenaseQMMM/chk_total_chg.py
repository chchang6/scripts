#!/usr/bin/env python
file = open('temp.out', 'r')
data = file.readlines()
file.close()
elements = []
elementdict = {'H':1, 'H_L':1, 'C':6, 'N':7, 'O':8, 'S':16}
for i in data:
   j = i.split()
   if j[0] != 'Bq':
      elements.append(j[0])
   elif j[0] == 'Bq':
      elements.append(j[-1])
sum = 0
for i in elements:
   try:
      if int(i):
         sum += int(i)
   except:
      sum += elementdict[i]
print sum
