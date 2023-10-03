# Following just needed to write out to JSON archive.
start_date='ddMmmYYYY'
end_date='ddMmmYYYY'

# Tasks

task_dict = {
'ID':'NAME',
'':'',
'':'',
'':'',
'':'',
'':'',
'':'',
}

# Daily constraints dictated by calendar and known fixed times
#   Days are 1-10 of pay period as even tuple indices (0-indexed)
#   None implies no constraints. Odd tuple indices are hours to charge.
apriori = { 'ID1': [1, 1.5, 3, 2., 4, 1., 5, 1., 6, 1., 8, 1.5, 9, 2., 10, 0.5],
            'ID2': [1, 2., 6, 1., 10, 1.],
            '': [3, 1., 4, 0.5],
            '': [5, 1.5],
            '': [1, 0.5, 2, 1., 8, 2.],
            '': [2, 0.5, 7, 0.5],
            '':[2, 0.5, 7, 0.5],
            #'HOLIDAY': [1, 8.],
            #'FLOAT': [8, 8., 9, 8.],
            #'PTO': [],
}
# Approximate hours. Values of 0 will draw from specific day requirements.
# This dict should rarely change and values should add up to 80.
targets = {
           'ID1': 22., 
           'ID2': 28.,
           '': 8.,
           '': 22.,
}

