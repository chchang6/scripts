#!/usr/bin/env python
# Convert gzipped text dumps of table from Lex to pandas dataframe and write out to Parquet file.

import gzip, re
from collections import namedtuple
import pandas as pd

def get_table_data(filehandle):
   data = []
   t = filehandle.readline()
   while re.match('^[0-9]', t):
      data.append(t.rstrip())
      t = filehandle.readline()
   return data

RE1 = re.compile('COPY public.projects_softwarerequests')
RE2 = re.compile('COPY public.projects_allocationrequest')
RE_header_open = re.compile('[^(]+\(')
RE_header_close = re.compile('\) FROM stdin;')

f = gzip.open('2022-01-21_12.gz', 'rt')
t = 'start'
while len(t) > 0:
   t = f.readline()
   if RE1.match(t):
      software_headers = RE_header_open.sub('', t.rstrip())
      software_headers = RE_header_close.sub('', software_headers)
      software_headers = [i.strip() for i in software_headers.split(',')]
      table = get_table_data(f)
      software_data = [i.rstrip().split('\t') for i in table]
      df_software = pd.DataFrame(software_data, columns=software_headers)
      df_software.drop(['id', 'essential', 'essential_yesno'], axis=1, inplace=True)
      df_software.replace(['\\N', 'N/A', '<NA>', 'Unknown','not sure'], pd.NA, inplace=True)
      df_software.replace('.*not accelerated.*', 'No', regex=True, inplace=True)
      df_software['usage'].replace(pd.NA, '0', inplace=True)
      df_software['gpu_quantity'].replace([pd.NA, '> 8'], ['0', '38'], inplace=True)
      df_software = df_software.astype({'name':'str', 'usage':'int', 'project_id':'int', 'code_source':'str', 'gpu_quantity':'int', 'gpu_ready':'str', 'gpu_speedup':'str', 'uses_mpi':'str', 'uses_openmp':'str'})
      df_software.replace(['Yes', 'No'], ['yes', 'no'], inplace=True)
      print(df_software)
   elif RE2.match(t):
      project_headers = RE_header_open.sub('', t.rstrip())
      project_headers = RE_header_close.sub('', project_headers)
      project_headers = [i.strip() for i in project_headers.split(',')]
      table = get_table_data(f)
      project_data = [i.rstrip().split('\t') for i in table]
      project_index = [int(i[0]) for i in project_data]
      df_projects = pd.DataFrame(project_data, index=project_index, columns=project_headers)
      df_projects.replace('\\N', pd.NA, inplace=True)
      t = df_projects.columns.drop(['project_handle', 'assigned_aus', 'allocation_cycle'])
      df_projects.drop(t, axis=1, inplace=True)
      print(df_projects)
f.close()

df_joined = df_software.join(df_projects, on='project_id', how='left')
df_joined.dropna(subset=['assigned_aus'], inplace=True)
print(df_joined)

df_joined.to_parquet('project_software.pqt', compression=None, index=False)

