#!/bin/bash --login
#SBATCH --job-name=test_selfkill
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=debug
#SBATCH --time=00:07:00
#SBATCH --account=hpcapps
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user christopher.chang@nrel.gov
#SBATCH --error=%x-%j.err
#SBATCH --output=%x-%j.out

cd /scratch/cchang
my_jobid=$SLURM_JOBID

if [ -f testfile ]
then
   rm testfile
fi
touch testfile
# Assume there is a job that takes N1 minutes.
# A logfile accumulates data, but the job may hang such that the file stops accumulating data.
# This tests whether a job can be killed from inside a background monitoring loop.


# Test condition runs loop until file gets large enough that we know it's large enough that it's past the hang.
while [ $(wc -c < testfile) -lt 161 ]
do
   # If the job has been running for a time >> what it takes to become larger than some limit,
   #   and the file is still small, kill job. Pretend time threshold is 1 minute.
   if [ $(wc -c < testfile) -lt 161 ] && [ $(squeue -j $my_jobid -o "%M" | tail -1 | awk -F ":" '{print $1}') -eq 1 ]
   then
      scancel $my_jobid
   else
      echo 'This is 16 bytes' >> testfile
      date # To monitor progress in loop
      # Increase sleep period to 7+ test job kill
      sleep 7
   fi
done &

# After the 11th iteration, file should be 11*16 = 176 bytes, so loop should be done.
# Sleep here to mimic the full job run. Pretend it's 5 minutes.
echo 'Running main routine'
sleep 300

