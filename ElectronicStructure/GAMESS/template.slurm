#!/bin/bash
#SBATCH --time=00:10:00
#SBATCH -N 2
#SBATCH --job-name GAMESStest
#SBATCH -p inter
#SBATCH --mail-type=all
#SBATCH --mail-user=

module unload mpi
module load mpi/
module load libraries/
module load gamess
SLURM_WORKING_DIR=`pwd`

# User parameters here
INPUT_FILE=$HOME/scratch/gamess/tests/exam09.inp         # GAMESS input file path. Job input file must have ".inp" extension.
OUTPUT_FILE=$SLURM_WORKING_DIR/exam09.log        # Desired logfile path
JOB_PPN=8           # Number of cores to use per node. Generally don't change unless memory limited
PROCS_PER_SOCKET=8  # Number of processes to be run per socket. Should be equal to $JOB_PPN.
MAX_TASKS_PER_NODE=$((2*$JOB_PPN))  # Don't change unless undersubscribing node.
# Specify path to scratch. Note that all GAMESS output files will be placed here, not in $USER/scr.
export SCR=/scratch/$USER/GAMESS_test
# The following deletes the above location, so if you're restarting a job, COMMENT THESE LINES OUT!!!
if [ -d $SCR ]
then
   rm -rf $SCR
fi
mkdir $SCR

# The user should usually not have to change anything below this line. Do so at your own risk.
export JOB_BASENAME=`basename $INPUT_FILE .inp`
cd $SCR

# Create hostlist
$GAMESS_DIR/parse_slurm_nodelist_GMS $SLURM_NODELIST $JOB_PPN

# The following does what rungms used to do, without the cruft.
cp $INPUT_FILE $SCR/$JOB_BASENAME.F05
source $GAMESS_DIR/GAMESS_EVs  # Feel free to copy the default file to your own location, modify, and source THAT file.
mpiexec -n $(($MAX_TASKS_PER_NODE*$SLURM_JOB_NUM_NODES)) --npersocket $PROCS_PER_SOCKET --hostfile goobers $GAMESS_DIR/gamess.00.x $JOB_BASENAME >& $OUTPUT_FILE
