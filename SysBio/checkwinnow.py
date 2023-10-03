#!/uhome/cchang/python2.5/bin/python
# Author Christopher Chang.
import re
RE1=re.compile(r'literal')
RE2=re.compile(r'indeterminable')
RE3=re.compile(r'KineticLaw')
RE4=re.compile(r'same units')
RE5=re.compile(r'<compartment> should be set to a value rather than be left undefined')
file=open('test1','r')
datalist = []
linecum = ''
for line in file:
   if line != "\n":
      linecum = linecum + line
   else:
      datalist.append(linecum)
      linecum = ''
file.close()
for x in datalist:
   if RE1.search(x) or RE2.search(x) or RE3.search(x) or RE4.search(x) or RE5.search(x):
#   if RE1.search(x):
      datalist.remove(x)
   else:
      print x
