#!/bin/bash --login
#SBATCH --time=06:00:00
#SBATCH -N 8
#SBATCH -n 64
#SBATCH --job-name O_0P95kVS8kwbrkO
#SBATCH --mail-user=
#SBATCH --mail-type=all

module load nwchem

PREFIX=$SLURM_JOBNAME
AUXFILES=''
JOBFILE=$PREFIX.nw
SCRAPFILES=''
SCRATCH=/home/chchang/scratch/$PREFIX

export SLURM_WORKING_DIR=`pwd`

nodes=$SLURM_JOB_NUM_NODES
corespn=8

if [ -d $SCRATCH ]
then
   rm -rf $SCRATCH
fi
mkdir $SCRATCH

cd $SCRATCH
cp $SLURM_WORKING_DIR/$JOBFILE .
for i in $AUXFILES
do
   cp $SLURM_WORKING_DIR/$i .
done

mpirun -np $(($nodes*$corespn)) numa_wrapper -ppn=$corespn nwchem $JOBFILE > $SLURM_WORKING_DIR/$PREFIX.out 2>&1

rm $SCRAPFILES
tar -cvzf keep$PREFIX.tgz *
cp keep$PREFIX.tgz $SLURM_WORKING_DIR/.

