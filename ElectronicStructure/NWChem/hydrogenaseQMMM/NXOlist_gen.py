#!/usr/bin/env python
import sys
if len(sys.argv) < 2:
   print "Usage: temp.py (alpha/beta)"
   sys.exit()
elif sys.argv[1] == 'alpha':
   file = open('aNXOlist', 'w')
elif sys.argv[1] == 'beta':
   file = open('bNXOlist', 'w')
else:
   print "Usage: temp.py (alpha/beta)"
   sys.exit()
# Write out doubly occupied orbital ranges
for i in range(50,146):
   file.write('%4i%c' % (i,'B'))
   file.write('\n')
for i in xrange(48):
   file.write('%4i%c' % (i+1,'B'))
   file.write('\n')
for i in range(146,150):
   file.write('%4i%c' % (i,'B'))
   file.write('\n')
for i in range(190,205):
   file.write('%4i%c' % (i,'B'))
   file.write('\n')
file.write('  98H\n')
# Spin-dependent orbitals
if sys.argv[1] == 'alpha':
   for i in range(170,181):
      file.write('%4i%c' % (i,'B'))
      file.write('\n')
elif sys.argv[1] == 'beta':
   file.write(' 170B\n')
   for i in range(180,190):
      file.write('%4i%c' % (i,'B'))
      file.write('\n')
file.close()
