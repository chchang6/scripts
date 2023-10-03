#!/usr/bin/env python
# Parse lmstat output for ANSYS licenses and report on current status

import subprocess
import re
from datetime import datetime
from time import sleep
from sys import exit

RE0a = re.compile('([0-9]+) licenses? issued')
RE0b = re.compile('([0-9]+) licenses? in use')
RE1 = re.compile('ansys:')
RE2 = re.compile('fluent:')

while True:
   a = subprocess.check_output(['lmstat.ansys']).split('\n')
   for i in a:
      if RE1.search(i):
         total_number_of_ansys_licenses = int(RE0a.search(i).group(1))
         number_of_used_ansys_licenses = int(RE0b.search(i).group(1))
      elif RE2.search(i):
         total_number_of_fluent_licenses = int(RE0a.search(i).group(1))
         number_of_used_fluent_licenses = int(RE0b.search(i).group(1))
   number_of_available_ansys_licenses = total_number_of_ansys_licenses - number_of_used_ansys_licenses
   number_of_available_fluent_licenses = total_number_of_fluent_licenses - number_of_used_fluent_licenses
   if number_of_available_ansys_licenses > 0 and \
      number_of_available_fluent_licenses > 0:
      print 'There are %i ANSYS and %i Fluent licenses available, exiting check' % (number_of_available_ansys_licenses, number_of_available_fluent_licenses)
      exit()
   elif number_of_available_ansys_licenses == 0:
      print 'No ANSYS licenses available as of ' + datetime.now().strftime('%c')
   elif number_of_available_ansys_licenses > 0 and number_of_available_fluent_licenses == 0:
      print 'No Fluent licenses available as of ' + datetime.now().strftime('%c')
   sleep(60)
 
