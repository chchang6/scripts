#!/bin/bash --login
#SBATCH --job-name=
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=36
#SBATCH --time=04:00:00
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --mail-user user.name@domain.name
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

ml use /nopt/nrel/apps/modules/test/modulefiles
ml q-chem/5.4

SCRATCH=/scratch/$USER/$SLURM_JOB_NAME
JOBFILE=$SLURM_JOB_NAME.qc
LOGFILE=$SLURM_JOB_NAME.log
mkdir $SCRATCH; chmod 700 $SCRATCH; cd $SCRATCH
cp $SLURM_SUBMIT_DIR/$JOBFILE .
echo "cd $SLURM_SUBMIT_DIR" > me
export QCSCRATCH=$SCRATCH

qchem -slurm -nt 36 $JOBFILE $LOGFILE save

