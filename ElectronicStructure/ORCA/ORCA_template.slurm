#!/bin/bash --login
#SBATCH --job-name=dimer_3d
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=18
#SBATCH --time=04:00:00
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user user.name@domain.name
#SBATCH --error=dimer3d-%j.err
#SBATCH --output=dimer3d-%j.out

# Run R(O)HF/RIMP2 at 4 nodes, 18 tasks/node, 4 hours
# Run NEVPT2 at 18 nodes, 2 tasks/node, 1 hour

module load orca/4.2.1

MAJOR_VERSION=
#MAJOR_VERSION=$SLURM_ARRAY_TASK_ID
MINOR_VERSION=3
#MINOR_VERSION=d$SLURM_ARRAY_TASK_ID
#case $SLURM_ARRAY_TASK_ID in
#1)
#   MINOR_VERSION=a
#   ;;
#2)
#   MINOR_VERSION=b
#   ;;
#3)
#   MINOR_VERSION=c
#   ;;
#4)
#   MINOR_VERSION=d
#   ;;
#5)
#   MINOR_VERSION=e
#   ;;
#6)
#   MINOR_VERSION=f
#   ;;
#7)
#   MINOR_VERSION=g
#   ;;
#*)
#   echo "Unexpected task ID $SLURM_ARRAY_TASK_ID" 
#   ;;
#esac

JOB_MAJOR=${SLURM_JOB_NAME:?}
JOB_BASENAME=${JOB_MAJOR}${MINOR_VERSION}
JOB_FILE=${JOB_BASENAME}.orc
SCRATCH=/scratch/cchang/$JOB_BASENAME
JOB_FILE_2=$JOB_BASENAME.inp
HHOSTFILE=$JOB_BASENAME.nodes
LOGFILE=$JOB_BASENAME.log
MOFILE_ORIG=none
#MOFILE_ORIG=$SLURM_SUBMIT_DIR/dimer_3c1.mp2nat
#MOFILE_ORIG=$SLURM_SUBMIT_DIR/dimer_3c2.gbw
MOFILE_SCRATCH=none
#MOFILE_SCRATCH=$SCRATCH/dimer_3c1.mp2nat
#MOFILE_SCRATCH=$SCRATCH/dimer_3c2.gbw
NUM_RANKS=`grep -A1 pal ${JOB_FILE} | tail -1 | tr -s " " | cut -d' ' -f3`

function prepare {
   tasks_per_node=`echo $SLURM_TASKS_PER_NODE | sed -r 's/\(.+\)//'`
   # Create convenience cd file
   mkdir $SCRATCH; cd $SCRATCH
   #cp $SLURM_SUBMIT_DIR/$JOB_FILE $SCRATCH/$JOB_FILE_2
   sed "s/   nprocs [0-9]*/   nprocs $SLURM_NTASKS/" $SLURM_SUBMIT_DIR/$JOB_FILE > $SCRATCH/$JOB_FILE_2
   if [ -f $MOFILE_ORIG ]
   then
      cp $MOFILE_ORIG $MOFILE_SCRATCH
      chmod 640 $MOFILE_SCRATCH
   fi
   # Create convenience cd file
   echo "cd $SLURM_SUBMIT_DIR" > me
   # Create hostfile
   if [ $NUM_RANKS -gt 1 ]
   then
      scontrol show hostnames > .temp
      for i in `cat .temp`
      do
         echo $i" slots="$tasks_per_node >> $SCRATCH/$HHOSTFILE
      done
      rm .temp
   fi
}

# Set up input files on all nodes
if [ -d $SCRATCH ]
then
   rm -rf $SCRATCH
fi
prepare
# Put a link mpirun on PATH and aliasing to orterun
cd $SCRATCH
export PATH=`pwd`:$PATH
ln -s `which orterun` mpirun
## Kick off run
`which orca` `pwd`/$JOB_FILE_2 "--bind-to socket" >& $LOGFILE

