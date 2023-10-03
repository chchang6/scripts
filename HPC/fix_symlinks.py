#!/usr/bin/env python

import os, sys
import re
import subprocess

RE1 = re.compile('(?<=\/)[^/]*(?=\/)')
RE2 = re.compile('\/usr\/')

t = subprocess.check_output(["find", ".", "-xtype", "l"])
t2 = t.decode('ascii').split('\n')
for bad_link in t2[:-1]:
   rellink = '../'*len(RE1.findall(bad_link))
   bad_target = os.readlink(bad_link)
   if not RE2.match(bad_target): continue
   proposed_target = RE2.sub(rellink, os.readlink(bad_link))
   print(bad_link, bad_target, proposed_target)
   os.remove(bad_link)
   os.symlink(proposed_target, bad_link)

