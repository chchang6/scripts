#!/usr/bin/env python
# Generate convenient ASCII string of specified length to use as index
#   for jobs, rather than using metadata for naming.

from random import getrandbits
from sys import stdout
import base64
import re

def rand1(leng):
    nbits = leng * 6 + 1
    bits = getrandbits(nbits)
    uc = u"%0x" % bits
    newlen = int(len(uc) / 2) * 2 # we have to make the string an even length
    ba = bytearray.fromhex(uc[:newlen])
    a = base64.urlsafe_b64encode(ba)[:leng]
    a = re.sub('-', '_', str(a, encoding='utf-8'))
    return a

print(rand1(16))

