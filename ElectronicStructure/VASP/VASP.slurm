#!/bin/bash
#SBATCH --job-name=
#SBATCH --nodes=1
#SBATCH --time=04:00:00
#SBATCH --mail-type=BEGIN,END,
#SBATCH --mail-user=user.name@domain.name
#SBATCH --error=%x-%j.err
#SBATCH --output=%x-%j.out

ml vasp/5.4.4

SCRATCH=/scratch/$USER/$SLURM_JOB_NAME
if [ ! -d $SCRATCH ]
then
   mkdir $SCRATCH
fi

cd $SCRATCH
for i in INCAR KPOINTS POSCAR POTCAR
do
   cp $SLURM_SUBMIT_DIR/$i  .
done

srun -n $SLURM_NPROCS vasp_gam >& LOG

