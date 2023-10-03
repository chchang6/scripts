#!/usr/bin/env python
# Script to create a charging plan based on overall constraints
#   for a 2-week reporting period.

import itertools, random
import pprint, copy
import datetime
import os.path, glob
from json import dump, dumps
import jsbeautifier
from sys import exit
from time import sleep
from timesheet_tasks import *
import re

#def get_list_of_past_files(path, year):
#   files = glob.glob(path + '/timesheet_*')
#   # Test for timesheets since beginning of current fiscal year
#   first_day = datetime.datetime(year, 10, 1, 0, 0, 0)
#   eligible_files = []
#   for i in files:
#      if datetime.datetime.strptime(i[0:30], path + '/timesheet_%d%b%Y') >= first_day:
#         eligible_files.append(i)
#   return eligible_files
#
#def task_charging_to_date(JSONfilelist):
#   charging_dict = {}
#   for i in JSONfilelist:
#      t = open(i, 'r'); t2 = t.read(); t.close()
#      while True:
#         if t2[0:13] == '"Timesheet: "': t2 = t2[13:]; break
#         else: t2 = t2[1:]
#      timesheet = loads(t2)
#      for day in timesheet:
#         for task in timesheet[day]:
#            if task not in charging_dict:
#               charging_dict[task] = timesheet[day][task]
#            else:
#               charging_dict[task] += timesheet[day][task]
#   return charging_dict

def rebalance(remdict, hours, key=None):
   # remdict is the data dictionary to rebalance
   # hours is the number of hours that need to be taken from tasks
   # key is excluded from consideration.
   # Take 1 hour at a time from random tasks.
   #print('Debug: enter rebalance')
   #print('Debug: Input dict')
   #print(f'Debug: key to exclude: {key}')
   #print(f'Debug: hours to rebalance: {hours}')
   t = sum(remdict.values())
   #print(f'Debug: Sum of hours to subtract from = {t}')
   #pp.pprint(remdict)
   keys = list(remdict.keys())
   if key: keys.remove(key)
   cycles = 0
   while round(hours,1) > 0.0:
      oldhours = copy.copy(hours)
      # Choose a key
      while True:
         k = random.choice(keys)
         if remdict[k] > 0.: break
      #print(f'Debug: I chose key {k} with remdict value {remdict[k]}')
      # Subtract at least an hour from task
      if hours >= 1.:
         if remdict[k] >= 1.:
            remdict[k] -= 1.
            hours -= 1.
         else: # hours is < 1 and remdict[k] < 1; since we're working with halves, both are 0.5
            hours -= remdict[k]
            remdict[k] = 0.
      else: # Fractional hour rebalance
         if remdict[k] >= hours:
            remdict[k] -= hours
            hours = 0.
         else:
            hours -= remdict[k]
            remdict[k] = 0.
      newhours = copy.copy(hours); cycles += 1
      if newhours == oldhours and cycles > 20:
         pp.pprint(remdict)
         exit('Too many rebalance cycles')
      elif newhours < oldhours:
         cycles = 1
      #print(f'Debug: Hours left to subtract from remdict = {hours}')
      #print(f'Debug: Sum of hours left in remdict = {sum(remdict.values())}')
   #print('Debug: Exit rebalance')
   return remdict

def rebalance_neg(remdict, targets, already_assigned, hours_left, key):
   # remdict is the data dictionary to rebalance
   # hours is the number of (negative) hours that need to be adjusted
   # key is the one with a negative value.
   # Take 1 hour at a time from random tasks.
   #print('Debug: Enter rebalance_neg')
   keys = list(remdict.keys())
   keys.remove(key)
   # Clean up any keys that are not in targets, as they are not relevant
   for i in range(len(keys)-1, -1, -1):
      if keys[i] not in targets.keys():
         keys.pop(i)
   #print("Debug rebalance_neg keys", keys)
   #print("Debug rebalance_neg remdict keys", remdict.keys())
   #print("Debug rebalance_neg targets keys", targets.keys())
   while round(hours_left,1) < 0.0:
      #print("Debug: keys is ", keys)
      k = random.choice(keys)#; print("Debug rebalance_neg random key = " + k)
      if hours_left <= -1.:
         # If I assign an hour, will I stay below hard target?
            # Have I already assigned more than the hard target?
            # Do I have more than an hour to rebalance?
         if remdict[k] + 1. <= targets[k] and \
            already_assigned[k] + 1. <= targets[k] and \
            remdict[k] >= 1.:
               remdict[key] += 1.; remdict[k] -= 1.; hours_left += 1.
         #print("Debug rebalance_neg whole hour remdict = ", remdict)
      else: # Fractional hour rebalance
         if remdict[k] + hours_left <= targets[k] and \
            already_assigned[k] + hours_left <= targets[k] and \
            remdict[k] >= abs(hours_left):
            remdict[key] -= hours_left; remdict[k] += hours_left; hours_left = 0.
         #print("Debug rebalance_neg fractional hour remdict = ", remdict)
   #print('Debug: Exit rebalance_neg')
   return remdict

#past_timesheets = get_list_of_past_files('timesheets', 2020)
#charges_to_date = task_charging_to_date(past_timesheets)

pp = pprint.PrettyPrinter(indent = 4)
#pp.pprint(charges_to_date)

# Re-jigger targets based on charges to date
#for i in charges_to_date:
#   if i not in targets: charges_to_date[i] = 0.
#total_planned_hours_to_date = sum([charges_to_date[i] for i in charges_to_date])
#multiplier = 80./total_planned_hours_to_date
#scaled_charged_hours_to_date = {}
#for i in targets:
#   try:
#      scaled_charged_hours_to_date[i] = multiplier * charges_to_date[i]
#   except KeyError: # Likely have not charged to target yet
#      scaled_charged_hours_to_date[i] = 0.
#balance = 0.
#continue_test = True
#pp.pprint(targets)
#j = 0
#while continue_test:
#   imbalance = 0.
#   for i in targets:
#      if targets[i] == 0.: continue
#      if abs(targets[i] - scaled_charged_hours_to_date[i]) > 0.5*targets[i]:
#         if targets[i] - scaled_charged_hours_to_date[i] > 0.: # Have been undercharging
#            targets[i] += 0.5
#         else: # Have been overcharging
#            targets[i] -= 0.5
#      imbalance += abs(targets[i] - scaled_charged_hours_to_date[i])
#   pp.pprint(targets)
#   j += 1
#   if j > 9 or imbalance < 10.: continue_test = False

# Check
#print('apriori')
#pp.pprint(apriori)

# Create running table of how many hours each project of interest has had assigned
assigned = {i:0. for i in apriori.keys()}
for i in targets.keys():
   if i not in assigned: assigned[i] = 0.
assert all([i < 8. for i in assigned.values()])

# Create dict of days. Assign constraints.
timesheet = {day:{task:0. for task in apriori.keys()} for day in range(1,11)}
for i in apriori:
   if apriori[i] is not None:
      for day,hours in zip(apriori[i][0::2], apriori[i][1::2]):
         timesheet[day][i] += hours
         # Subtract assigned hours from each task in targets
         assigned[i] += hours

# Check
#print('assigned')
#pp.pprint(assigned)
#print('Sum of assigned: {}'.format(sum(assigned.values())))

# Create remaining table for apriori.
remaining = copy.copy(assigned)
for i in assigned:
   if i in targets.keys(): # There is an expected amount
      remaining[i] = targets[i] - assigned[i]
#      if remaining[i] < 0.: # There is more assigned already than target, so don't assign any more.
#         remaining[i] = 0.
   else: # There is not a target amount, so don't assign. 
      remaining[i] = 0.

# Check
print('Intermediate remaining')
pp.pprint(remaining)
print('Sum of intermediate remaining: {}'.format(sum(remaining.values())))

# Rebalance for those tasks that were assigned, but not in targets
for i in assigned:
   if i not in targets.keys() and assigned[i] > 0.:
      remaining = rebalance(remaining, assigned[i], i)

# 121620: Add block to see if assigned is already at exactly 80.

# Rebalance for those tasks that were overassigned
for i in remaining:
   if round(remaining[i], 1) < 0.0: # Significantly negative, rebalance
      remaining = rebalance_neg(remaining, targets, assigned, remaining[i], i)
   elif remaining[i] < 0.: # Less significant, just zero out
      remaining = 0.

# Check
#print('remaining')
#pp.pprint(remaining)
#print('Sum of remaining: {}'.format(sum(remaining.values())))

# Now go through timesheet day by day; if there are less than 8 hours
#   already assigned, pull 1 hour from a random task with time left.
#   Continue until day is full, then move on.
# Check timesheet
#print("Timesheet before main loop")
#pp.pprint(timesheet)
for day in timesheet:
   t = 0.
   for task in timesheet[day].keys():
      t += timesheet[day][task]
   assert(t <= 8.), "Day {} has too many hours to start: {}".format(day, t)

for day in timesheet:
   assigned_today = sum([timesheet[day][task] for task in timesheet[day].keys()])
   assert assigned_today <= 8.
   keys = list(remaining.keys())
   while round(assigned_today, 1) < 8.0:
      try:
         assert(int(sum(remaining.values())) >= 0), 'Ran out of time to assign'
      except AssertionError:
         pp.pprint(timesheet)
         exit()
      k = random.choice(keys)#; print("Debug main loop k = ", k)
      #print("Debug main loop remaining: ", remaining)
      if remaining[k] >= 1.:
         if assigned_today <= 7.:
            assignment = 1.
         elif assigned_today > 7.:
            assignment = 8. - assigned_today
      elif remaining[k] < 1.:
         if assigned_today > (8. - remaining[k]):
            assignment = 8. - assigned_today
         elif assigned_today <= (8. - remaining[k]):
            assignment = remaining[k]
      timesheet[day][k] += assignment
      remaining[k] -= assignment
      assigned_today += assignment
      assert assigned_today <= 8.
      #print('day: {}, assigned_today: {}'.format(day, assigned_today))
      #pp.pprint(timesheet[day])

pp.pprint(timesheet)
# Check
print('Hours assigned per task')
t = {task_dict[task]:0. for task in remaining.keys()}
for i in timesheet:
   for j in timesheet[i]:
      t[task_dict[j]] += timesheet[i][j]
pp.pprint(t)
print('Total: {}'.format(sum(t.values())))

# Dump out timesheet to JSON for record
if os.path.exists('timesheet_{}_{}'.format(start_date, end_date)):
   test = input('Timesheet for this time period exists. Do you want to \
overwrite the JSON record? (y/n)')
   if test == 'y': pass
   elif test == 'n': exit()
   else: exit('Don\'t recognize response')
outfile = open('timesheet_{}_{}'.format(start_date, end_date), 'w')
dump('Start date = ' + start_date, outfile)
outfile.write('\n')
dump('End date = ' + end_date, outfile)
outfile.write('\n')
dump('Task dictionary: ', outfile)
dump(task_dict, outfile, indent=4)
outfile.write('\n')
dump('Apriori: ', outfile)
t = dumps(apriori, indent=4)
t = re.sub('\[\n {7}', '[', t)
t = re.sub('(?<!\]),\n {7}', ',', t)
t = re.sub('\n {4}\]', ']', t)
outfile.write(t)
outfile.write('\n')
dump('Timesheet: ', outfile)
dump(timesheet, outfile, indent=4)
outfile.close()
