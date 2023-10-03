export LARGE_FILES="TRUE"
export FC=ifort
export CC=icc
#export USE_GPROF=yes # Put profiling/debugging handles in
#export USE_SUBGROUPS=yes # Don't know what this one does yet
export CFLAGS="-I/usr/include/python2.4"
export CXXFLAGS="-I/usr/include/python2.4"
export TCGRSH="/usr/bin/ssh"
export NWCHEM_TOP="/home/cchang/nwchem-5.1.1"
export NWCHEM_TARGET="LINUX64"
#export TARGET="LINUX64" # For Global arrays 4.1b build only
#export OLD_GA=yes  # Use an older version of the GA libraries?
#export MSG_COMMS=MPI # ?
export NWCHEM_MODULES="pnnl"
export USE_MPI="y"
export USE_MPIF="y"
export USE_MPIF4="y"  # Use 4-byte integers in PW code
#export OMPI_F77="gfortran"
#export OMPI_FC="gfortran"
#export LIBMPI="-lmpich -lmpichf90" # MPICH-2
export MPI_INCLUDE="/apps/x86_64/mpi/openmpi/intel-11.1-f046-c046/openmpi-1.3.4a1r21977_oobpr/include"
export MPI_LIB="/apps/x86_64/mpi/openmpi/intel-11.1-f046-c046/openmpi-1.3.4a1r21977_oobpr/lib"
export LIBMPI="-lmpi_f90 -lmpi_f77 -lmpi -lopen-rte -lopen-pal -lnsl -lm"
export ARMCI_DEFAULT_SHMMAX=16777216
export ARMCI_NETWORK="OPENIB"
export IB_HOME="/usr"
export IB_INCLUDE="$IB_HOME/include"
export IB_LIB="$IB_HOME/lib64"
export IB_LIB_NAME="-libverbs"
export USE_PYTHON64=y  # Forces use of 64-bit libraries. Value isn't checked, so comment this line out for 32-bit,
export PYTHONHOME="/usr"
export PYTHONVERSION="2.4"
export HAS_BLAS="no"
# Optimized BLAS usage
#export USE_64TO32="y"
#export BLASOPT=$BLASLIB
#export BLAS_LIB="-L/copt/2.0/ATLAS/3.8.1/lib64 -lptf77blas -latlas" # For Global arrays build only
# Some example make statements from Yan Li, message posted 5/27/2011
#make DIAG=PAR FC=gfortran CC=gcc CDEBUG="-g -ffpe-trap=invalid,zero,overflow" FDEBUG="-g -ffpe-trap=invalid,zero,overflow" FOPTIMIZE="-g -ffpe-trap=invalid,zero,overflow" COPTIMIZE="-g -ffpe-trap=invalid,zero,overflow" nwchem_config
#make DIAG=PAR FC=gfortran CC=gcc CDEBUG="-g -ffpe-trap=invalid,zero,overflow" FDEBUG="-g -ffpe-trap=invalid,zero,overflow" FOPTIMIZE="-g -ffpe-trap=invalid,zero,overflow" COPTIMIZE="-g -ffpe-trap=invalid,zero,overflow" $1
#make DIAG=PAR FC=gfortran CC=gcc CDEBUG="-pg -g" FDEBUG="-pg -g" FOPTIMIZE="-pg -g -O0" COPTIMIZE="-pg -g -O0" nwchem_config
#make DIAG=PAR FC=gfortran CC=gcc CDEBUG="-pg -g" FDEBUG="-pg -g" FOPTIMIZE="-pg -g -O0" COPTIMIZE="-pg -g -O0" $1
#make DIAG=PAR FC=gfortran CC=gcc nwchem_config make DIAG=PAR FC=gfortran CC=gcc nwchem_config make DIAG=PAR FC=gfortran CC=gcc $1

# For 32-bit integer down-conversion
#   1) cd $NWCHEM_TOP/src
#   2) make clean
#   3) make 64_to_32
#   4) make USE_64TO32=y HAS_BLAS=yes BLASOPT=" optimized BLAS"

