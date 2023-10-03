#!/usr/bin/python
infile = open('temp','r')
data = infile.readlines()
infile.close()
keylist = []
dict = {}
for a in data:
   b = a.strip().split()
   Key = float(b[-1])
   keylist.append(Key)
   dict[Key] = b[0:-1]
keylist.sort()
keylist.reverse()
for c in keylist:
   for d in dict[c]:
      print d,
   print c
