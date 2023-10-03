#!/usr/bin/env python

from multiprocessing import Process

def function():
   print 'Here'
   return

process_list = []
for i in xrange(2):
    p = Process(target=function, name=i+1)
    p.start()
    process_list.append(p)

for i in range(2,0,-1):
    print 'Process ' + str(process_list[i-1].name) + ' alive? ' + str(process_list[i-1].is_alive())
    print 'My name is process ' + str(process_list[i-1].name)
    process_list[i-1].join()
    print 'After joining, process ' + str(process_list[i-1].name) + ' alive? ' + str(process_list[i-1].is_alive())
    print 'Popping ',
    print process_list.pop(i-1)

print 'Length of process list is ' + str(len(process_list))

