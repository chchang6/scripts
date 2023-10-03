#!/bin/bash --login
#SBATCH --job-name=5_metethytcene
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=18
#SBATCH --time=04:00:00
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user user.name@domain.name
#SBATCH --error=cpscf-%j.err
#SBATCH --output=cpscf-%j.out

function prepare {
   # Create hostfile
   if [ $NUM_RANKS -gt 1 ]
   then
      if [ $SLURM_NNODES -eq 1 ]
      then
         echo $SLURMD_NODENAME" slots="$RANKS_PER_NODE >> $SLURM_SUBMIT_DIR/$HHOSTFILE
         cp $SLURM_SUBMIT_DIR/$JOB_FILE $SCRATCH/$JOB_FILE_2
         if [ -f $SLURM_SUBMIT_DIR/$MOFILE ]
         then
            cp $SLURM_SUBMIT_DIR/$MOFILE $SCRATCH/$MOFILE
         fi
      else
         scontrol show hostnames > .temp
         for i in `cat .temp`
         do
            echo $i" slots="$RANKS_PER_NODE >> $SLURM_SUBMIT_DIR/$HHOSTFILE
         done
         rm .temp
      fi
   fi
}

module load orca/4.2.0

MAJOR_VERSION=2
MINOR_VERSION=
JOB_MAJOR=${SLURM_JOB_NAME:?}_$MAJOR_VERSION
JOB_BASENAME=${JOB_MAJOR}${MINOR_VERSION}
JOB_FILE=${JOB_BASENAME}.orc
SCRATCH=/scratch/cchang/$JOB_BASENAME
JOB_FILE_2=$JOB_BASENAME.inp
HHOSTFILE=$JOB_BASENAME.nodes
LOGFILE=$JOB_BASENAME.log
MOFILE=$JOB_MAJOR.gbw
NUM_RANKS=`grep -A1 pal ${JOB_FILE} | tail -1 | tr -s " " | cut -d' ' -f3`

# Test if serial or parallel
if [ $NUM_RANKS -gt 1 ]
then
   # Parallel. Multiple nodes?
   if [ $SLURM_NNODES -eq 1 ]
   then
      # No. Spread ranks over cores on 1 node.
      RANKS_PER_NODE=$NUM_RANKS
   else
      # Yes. Spread ranks over several nodes, and set up local scratch on each.
      RANKS_PER_NODE=$((NUM_RANKS/SLURM_NNODES))
   fi
   CORES_PER_RANK=$((36/RANKS_PER_NODE))
fi

#CPUMASK=`map_cores_to_ranks.py $RANKS_PER_NODE 2`

# Put a link mpirun on PATH and aliasing to orterun
if [ -d $SCRATCH ]
then
   rm -rf $SCRATCH
fi
mkdir $SCRATCH
cp $JOB_FILE $SCRATCH/$JOB_FILE_2
cd $SCRATCH
export PATH=`pwd`:$PATH
ln -s `which orterun` mpirun
# Kick off run
`which orca` `pwd`/$JOB_FILE_2 --report-bindings --bind-to=socket >& $LOGFILE
#pdsh -w $SLURM_JOB_NODELIST hostname; ls $SCRATCH

