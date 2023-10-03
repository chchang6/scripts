#!/bin/bash --login
#SBATCH --time=04:00:00
#SBATCH -N 4
#SBATCH -n 32
#SBATCH --job-name test
#SBATCH --mail-type=ALL
#SBATCH -p pbatch 

nodes=$SLURM_JOB_NUM_NODES
cores=8

cd /home/cchang/nwchem-5.1.1/QA
export NWCHEM_TOP=/home/cchang/nwchem-5.1.1
export NWCHEM_TARGET=LINUX64
export NWCHEM_EXECUTABLE=$NWCHEM_TOP/bin/LINUX64/nwchem
./doqmtests.mpi $(($nodes*$cores)) >& qmtests.log
./runtests.md >& mdtests.log

