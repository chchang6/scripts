#!/usr/bin/env python

import re
file = open('input.nw', 'r')
numbers = {'H':0, 'C':0, 'N':0, 'O':0, 'S':0, 'Fe':0}
status = False
while True:
   data = file.readline()
   if re.match('geometry', data):
      status = True
   if status == True:
      if data[0] == 'H': numbers['H'] = numbers['H'] + 1
      elif data[0:3] == 'H_L': numbers['H'] = numbers['H'] + 1
      elif data[0] == 'C': numbers['C'] = numbers['C'] + 1
      elif data[0] == 'N': numbers['N'] = numbers['N'] + 1
      elif data[0] == 'O': numbers['O'] = numbers['O'] + 1
      elif data[0] == 'S': numbers['S'] = numbers['S'] + 1
      elif data[0:2] == 'Fe': numbers['Fe'] = numbers['Fe'] + 1
      elif data[0:3] == 'end':
         break
print numbers
