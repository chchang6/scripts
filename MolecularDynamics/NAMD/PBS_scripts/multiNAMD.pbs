#!/bin/bash --login

#PBS -N multiNAMD
#PBS -q Std
#PBS -l nodes=1:ppn=1
#PBS -l walltime=08:00:00
#PBS -m abe
#PBS -M user.name@domain.name
#PBS -e ./pbs.err
#PBS -o ./pbs.out

module load namd2

cd $PBS_O_WORKDIR

./multiNAMD.sh

#NODES=`cat $PBS_NODEFILE`
#NODELIST=$PBS_TMPDIR/namd2.nodelist
#echo group main >! $NODELIST
#for node in $NODES; 
#  do
#  echo host $node >> $NODELIST
#done

#charmrun `which namd2` +p$PBS_NPROCS ++nodelist $NODELIST minimize.namd > minimize.log
