#!/usr/bin/env python

import os
from sys import exit
from random import randint

length=12
return_string = ''
for i in xrange(length):
   return_string += chr(randint(33,126))  # Returns printable characters in 7-bit ASCII range

home_dir = os.getenv('HOME')
test = os.listdir(home_dir)
if '.mpd.conf' in test and '.mpdpasswd' in test: exit()  # Necessary files already exist
else:  # First time user is running mpiexec from MVAPICH2
   file = open(home_dir + '/.mpd.conf', 'w')
   file.write('secretword=' + return_string + '\n')
   file.close()
   file = open(home_dir + '/.mpdpasswd', 'w')
   file.write('secretword=' + return_string + '\n')
   file.close()
os.chmod(home_dir + '/.mpd.conf', 384)
os.chmod(home_dir + '/.mpdpasswd', 384)
