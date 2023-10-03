#!/usr/bin/python
# Python script to grab every 10th line of an input file.
# CHC 1/6/05.
import sys
lines = sys.stdin.readlines()
sys.stdout.writelines(lines[:1])
for lineIndex in range(1, len(lines), 10):
   sys.stdout.write(lines[lineIndex])
