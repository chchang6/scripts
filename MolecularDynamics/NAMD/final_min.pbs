#!/bin/bash --login

#PBS -N finalmin_4
#PBS -q Default
#PBS -l nodes=4:ppn=2
#PBS -l walltime=08:00:00
#PBS -m abe
#PBS -M user.name@domain.name
#PBS -e ./namd2.err.pbs
#PBS -o ./namd2.out.pbs

module load namd2

cd $PBS_O_WORKDIR

NODES=`cat $PBS_NODEFILE`
NODELIST=$PBS_TMPDIR/namd2.nodelist
echo group main >! $NODELIST
for node in $NODES; 
  do
  echo host $node >> $NODELIST
done

charmrun `which namd2` +p$PBS_NPROCS ++nodelist $NODELIST final_min.namd > final_min.log
