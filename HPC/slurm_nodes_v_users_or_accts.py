#!/usr/bin/env python

import subprocess as sp
import pandas as pd
from sys import exit

def regroup(dataframe, group_category, total_job_lower_limit, summary_string):
   if summary_string == 'sum':
      t = dataframe.groupby(by=group_category)['NumNodes'].sum()
      t2 = dataframe.loc[dataframe['JobStatus']=='RUNNING'].groupby(group_category)['NumNodes'].sum()
      t3 = dataframe.loc[dataframe['JobStatus']=='PENDING'].groupby(group_category)['NumNodes'].sum()
   elif summary_string == 'count':
      t = dataframe.groupby(by=group_category)['NumNodes'].count()
      t2 = dataframe.loc[dataframe['JobStatus']=='RUNNING'].groupby(group_category)['NumNodes'].count()
      t3 = dataframe.loc[dataframe['JobStatus']=='PENDING'].groupby(group_category)['NumNodes'].count()
   df2 = pd.DataFrame({'Total':t, 'Running': t2, 'Pending': t3})
   df2.fillna(0, inplace=True)
   df2 = df2.astype({'Running':int, 'Pending':int}) 
   df2.sort_values(by = 'Total', inplace=True, ascending=False)
   return df2.loc[df2['Total'] > total_job_lower_limit]

def regroup_2level(dataframe, group_category1, group_category2):
   t = dataframe.groupby([group_category1, group_category2]).count()
   return t

t = sp.run(['squeue', '--format=%15u%12T%10D%16a%P'], capture_output=True)
data = str(t.stdout).split('\\n')
job_list = []
for i in data[1:-1]:
   user, status, node_string, account, partition = i.split()
   job_list.append((user, account, status, int(node_string), partition))

df = pd.DataFrame.from_records(job_list, columns = ['User', 'Account', 'JobStatus', 'NumNodes', 'Partition'])
lower_limit = 50
print(f'Jobs by user if more than {lower_limit}')
t = regroup(df, 'User', lower_limit, 'count')
print(t); print()
print(f'Jobs by account if more than {lower_limit}')
t = regroup(df, 'Account', lower_limit, 'count')
print(t); print()
print(f'Nodes by user if more than {lower_limit}')
t = regroup(df, 'User', lower_limit, 'sum')
print(t); print()
print(f'Nodes by account if more than {lower_limit}')
t = regroup(df, 'Account', lower_limit, 'sum')
print(t); print()
print('Job breakdown by partition')
lower_limit = 0
t = regroup_2level(df, 'Partition', 'JobStatus')
print(t['User']); print()

