#!/usr/bin/env python
# Script to read in XPath output from Oxygen containing the paths to file attachments (rooted at the containing folder level),
#   and compare that to the contents of the PDF directory. If a folder name is present in the PDF directory that is not
#   referenced in the XPath output, that means it is an orphan attachment. From the printed list of directory names, can
#   move them elsewhere and enter reference concerned is necessary + reattach.  CHC 7/21/10

import os, re

file = open('test_xpath', 'r')
data = file.readlines()
file.close()

data2 = []

for i in data:
   if re.search('internal-pdf', i):
      data2.append(i.strip())
data = data2

too_many_files = os.listdir('.')
libURLs = []
for i in data:
   libURLs.append(re.sub('^.*\/(.+)\/.*', '\g<1>', i))
for i in too_many_files:
   if i not in libURLs:
      print i
