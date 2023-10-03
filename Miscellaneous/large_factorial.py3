#!/usr/bin/env python
#  Calculate large factorials by adding up logs of factors,
#     then expressing to limited precision in scientific notation.
#     Mostly to get order-of-magnitude estimates.

import sys, re
import math

test = True
while test:
   base = input('What factorial? ')
   if re.search('[^0-9]', base):
      print('Input must be an integer!')
   else:
      base = int(base)
      test = False

a = range(1,base+1)
c = math.fsum([math.log10(i) for i in a])
parts = math.modf(c)
print('{0} E+{1}'.format(math.pow(10, parts[0]), int(parts[1])))
