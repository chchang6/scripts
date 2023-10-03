#!/usr/bin/env python
# Script to take KR's alloc_tracker output and parse to spreadsheet format.

# To turn off DISPLAY requirement on cluster
import matplotlib
matplotlib.use('Agg')


from subprocess import Popen, PIPE
import numpy
import matplotlib.pyplot as plt

class project:
   def __init__(self, handle, total_allocated, total_used, total_forfeited, FY_remaining, area):
      self.area = area
      self.handle = handle
      self.allocated = total_allocated
      self.used = total_used
      self.forfeit = total_forfeited
      self.remaining = FY_remaining

data = Popen(['alloc_tracker', '--showall', '--drillbyaccount'], stdout=PIPE).communicate()
data = data[0].split('\n')
category = None
allocation_list = []
for i in xrange(len(data)): # Hard limits, depends on projects; double-check
   #print 'Is this a plus? ' + i[0]
   if data[i][0:4] == 'Area':
      for j in range(i+2, len(data)):
         if data[j][0] == '+':
            #print 'If so, should be part of a category: ' + str(category)
            if category != 'noarea':
               t = data[j][1:].split()
               allocation_list.append(project(t[0], int(t[1]), int(t[2]), int(t[3]), int(t[4]), category))
         elif data[j][0:4] == '----':
            break
         else:
            category = data[j][0:6]
            #print 'If not, then set the category'
            #print 'Set new category to ' + category
CSlist = []
for i in allocation_list:
   if i.area == 'Comput': CSlist.append(i)
allocation_list = CSlist
handles = []
xpos = numpy.arange(0,2*len(allocation_list),2)
barwidth = 1
frac_used = numpy.zeros( (len(allocation_list)), numpy.float )
frac_forfeited = numpy.zeros( (len(allocation_list)), numpy.float )
for i in xrange(len(allocation_list)):
   handles.append(allocation_list[i].handle)
   frac_used[i] = float(allocation_list[i].used) / float(allocation_list[i].allocated)
   frac_forfeited[i] = float(allocation_list[i].forfeit) / float(allocation_list[i].allocated)
plot_used = plt.bar(xpos, frac_used, barwidth, color='b')
plot_forfeit = plt.bar(xpos, frac_forfeited, barwidth, color='g', bottom=frac_used)
plt.xlabel('Project')
plt.ylabel('Fraction')
plt.xticks(xpos+0.5*barwidth, tuple(handles), rotation=-89)
plt.xlim([-0.5,2*len(allocation_list)])
plt.tight_layout()
plt.legend( (plot_used[0], plot_forfeit[0]), ('Used', 'Forfeited'), loc='upper left')
figure = plt.gcf()
figure.set_size_inches(8,4)
plt.savefig('CSalloc_usedforf.png', dpi=300)
