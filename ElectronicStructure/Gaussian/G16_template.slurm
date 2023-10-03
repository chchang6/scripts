#!/bin/bash --login
#SBATCH --job-name=ABCDEF_1a1
#SBATCH --nodes=1
#SBATCH --time=04:00:00
#SBATCH --mail-user user.name@domain.name
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --error=%x-%j.err
#SBATCH --output=%x-%j.out

module load gaussian/G16C

JOB_FILE=${SLURM_JOB_NAME:?}.gjf
#CHKFILE=chkfile_name.chk
SCRATCH=/scratch/$USER/$SLURM_JOB_NAME
SCRATCH2=/tmp/scratch
export GAUSS_SCRDIR=$SCRATCH2

mkdir $SCRATCH; chmod 700 $SCRATCH
cd $SLURM_SUBMIT_DIR
cp $JOB_FILE $SCRATCH/.
#cp $CHKFILE $SCRATCH/.; chmod 640 $SCRATCH/$CHKFILE
cd $SCRATCH
echo "cd $SLURM_SUBMIT_DIR" > me

if [ $SLURM_JOB_NUM_NODES -gt 1 ]
then
   g16dir=`which g16`
   cp `dirname $g16dir`/Default.Route .
   export GAUSS_LFLAGS='-vv -opt "Tsnet.Node.lindarsharg: ssh"'
   export GAUSS_EXEDIR=$g16root/g16/linda-exe:$GAUSS_EXEDIR
   linda_slurm.py $JOB_FILE
fi

g16 $JOB_FILE
find /tmp/scratch -user $USER -exec rm -f '{}' \;
ipcrm -a

