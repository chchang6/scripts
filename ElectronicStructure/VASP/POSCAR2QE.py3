#!/usr/bin/env python3

from numpy import cumsum, argmax

file = open('POSCAR', 'r')
data = file.readlines()
file.close()

elements = data[0].strip().split()
numbers = [int(i) for i in data[5].strip().split()]
endpoints = cumsum(numbers)

def element(index):
   return elements[argmax(index < endpoints)]
   
for i in range(7,len(data)):
   t = data[i].strip().split()
   print(' {:3s}{:20.16f}{:20.16f}{:20.16f}'.format(element(i-7), float(t[0]), float(t[1]), float(t[2])))

