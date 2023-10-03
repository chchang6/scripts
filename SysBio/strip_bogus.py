#!/usr/bin/env python
import xml.dom.minidom, sys

class unicodeWriter:
   def write(self, data):
      sys.stdout.write(data.encode('utf-8'))

document = xml.dom.minidom.parse('C_rein_fermentation_v2.3test.xml')
elementlist = ['compartment', 'parameter', 'initialAssignment', 'assignmentRule', 'species']
for i in elementlist:
   elements = document.getElementsByTagName(i)
   for j in elements:
      if j.hasAttribute('bogus'):
         j.removeAttribute('bogus')
document.writexml(unicodeWriter())
