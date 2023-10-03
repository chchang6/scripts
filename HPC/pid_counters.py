#!/usr/bin/env python
# Example output single-threaded
#Process data
#[ (59055356940L, 46069, '(g09)', 'S', 46068, 46068, 36352, 34869, 46068, 4202496L, 642L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 20L, 0L, 1L, 0L, 87574065L, 98594816L, 254L, 18446744073709551615L, 4194304L, 4455772L, 140737370957552L, 140737370926832L, 228804183918L, 0L, 65536L, 16781318L, 0L, 18446744071579314580L, 0L, 0L, 17, 5, 0L, 0L, 0L, 0L, 0L, 24071, 254, 196, 64, 0, 21320, 0)]
#Threads data
#46069 [ (59055357129L, 46069, '(g09)', 'S', 46068, 46068, 36352, 34869, 46068, 4202496L, 642L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 20L, 0L, 1L, 0L, 87574065L, 98594816L, 254L, 18446744073709551615L, 4194304L, 4455772L, 140737370957552L, 140737370926832L, 228804183918L, 0L, 65536L, 16781318L, 0L, 18446744071579314580L, 0L, 0L, 17, 5, 0L, 0L, 0L, 0L, 0L)]
# 46069 = process ID
# 

def formatPrint(dataProcess, dataThreads):
    '''
    Formats print.
    dataProcess: numpy array
         process data array (dtype = typeProc)
    dataThreads: dictionary
         threads data dictionary consists of thread data numpy arrays (dtype = typeThread)
    '''
    print 'Process data'    
    print dataProcess
    print 'Threads data'
    for k in dataThreads.keys():
        print k, dataThreads[k]

def getLastRecord (dataProcess, dataThreads, procQuery, threadsQuery, prevProcData, prevThreadsData):
    '''
    Prints data for last update time interval.
    dataProcess: numpy array
         process data array (dtype = typeProc)
    dataThreads: dictionary
         threads data dictionary consists of thread data numpy arrays (dtype = typeThread)
    procQuery: list
         name list of process counters
    threadsQuery: list
         name list of thread counters
    prevProcData: numpy array
         process data array (dtype = typeProc) with length = 1
    prevThreadsData: dictionary
         threads data dictionary consists of thread data numpy arrays (dtype = typeThread) with length = 1  
    '''    
    import pyrfcon
    dataProcess, dataThreads = pyrfcon.parseQuery (dataProcess, dataThreads, procQuery, threadsQuery, prevProcData, prevThreadsData)
    formatPrint(dataProcess, dataThreads);
   
def printUsage():
  print '''
Usage:
  example.py <program> [<arg1> [<arg2> [...]]]
'''

if __name__ == "__main__":
  import sys
  import subprocess
  import time
  import pyrfcon
 
  '''You can construct different queries from standard and extra (cpuUsage, memUsage) counters.'''
  procQuery = ['time', 'Working Set' , 'cpuUsage', 'memUsage']
  threadsQuery = ['time', 'cpuUsage']  
 
  if len(sys.argv) < 2:
    printUsage()
    sys.exit(-1)
 
  '''Start new process, e.g. pid_monitor.py g09 input.com'''
  process = subprocess.Popen(sys.argv[1:4])
  pid = process.pid
 
  '''
  Attach to already running process (for example to process with PID = 228)
  pid = 41336
  '''
 
  '''
  To start to monitor process and its threads, you must first create MonitorThread object.
  By default MonitorThread saves the process info every 0.5 seconds, but you can set necessary updateInterval (in seconds).
  '''
  updateInterval = 0.7
  thread = pyrfcon.MonitorThread(pid, updateInterval)
 
  '''Start the thread's activity'''
  thread.start()
 
  '''Using getData() function'''
  thread.startCollectData()
  time.sleep(5)
  dataProcess, dataThreads = thread.getData(procQuery, threadsQuery)
  formatPrint(dataProcess, dataThreads);
  time.sleep(5)
  dataProcess, dataThreads = thread.getData()
  formatPrint(dataProcess, dataThreads);
  time.sleep(5)
  thread.stopCollectData()
  dataProcess, dataThreads = thread.getData(procQuery)
  formatPrint(dataProcess, dataThreads);
 
  '''Using callback'''
  thread.setCallback(getLastRecord)
  time.sleep(5)
  thread.setCallback(getLastRecord, procQuery, threadsQuery)
  time.sleep(5)
  thread.setCallback(getLastRecord)
  time.sleep(5)
  thread.clearCallback()

  '''Wait for child process to terminate'''
  process.wait()

  '''Stop collect data'''
  thread.setProcess(False)
 
  '''Wait until the thread terminates'''
  thread.join()

