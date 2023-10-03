#!/usr/bin/env python

def eng_float(float_string):
   # Convert 1.23456E+12 to .123456E+13
   t = float_string.split('E+')  # Here safe to assume numbers > 1
   exponent = int(t[1]) + 1
   abcissa = t[0] = '.' + t[0][0] + t[0][2:]
   exponent = '%02i' % exponent
   return abcissa + 'E+' + exponent

logfile = ''
frequencies = []
file = open(logfile, 'r')
while True:
   t = file.readline()
   if t[0:12] == ' Frequencies':
      t2 = t.rstrip().split()[2:]
      frequencies.extend([float(i) for i in t2])
   elif t == '':
      break
file.close()

print 'Number of frequencies: ' + str(len(frequencies))
frequencies.reverse()
for i in xrange(len(frequencies)/4):
   for j in xrange(4):
      t = eng_float('%.9E' % (frequencies[4*i + j]))
      print '%19s' % t,
   print
for i in xrange(len(frequencies) % 4):
   t = eng_float('%.9E' % (frequencies[4*(len(frequencies)/4) + i]))  # Watch integer math
   print '%19s' % t,
print
