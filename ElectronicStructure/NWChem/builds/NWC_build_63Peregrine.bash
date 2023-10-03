# Source this file to set the necessary environment variables to build NWChem.
#   General procedure after that is
#     make nwchem_config
#     make
#   Note that line 837 in src/tools/config/makefile.h needs to be manually changed to "icc" if a pure Intel build wanted.
#     otherwise, you will see some gcc calls at the start of the build.
#   Same for line 544 in src/tools/armci/config/makefile.h
#   Error "No rule to make ...typesf2c.h' overcome by copying everything in src/tools/include into src/include. Error arises from using variable INCDIR (which points to src/include, and includes the "-I" flag) when INCPATH is needed instead (which points to src/tools/include, and does NOT contain the -I).

export LARGE_FILES="TRUE"
export FC=ifort
export CC=icc
export CPPFLAGS='-DCCSDTQ'
export CFLAGS="-I/projects/nrel/apps/python/Python-2.7/include/python2.7"
export CXXFLAGS="-I/projects/nrel/apps/python/Python-2.7/include/python2.7"
export TCGRSH="/usr/bin/ssh"
export NWCHEM_TOP="/nopt/nrel/apps/.nwchem/dist/nwchem-6.3.revision2-src.2013-10-17"
export NWCHEM_TARGET="LINUX64"
#export TARGET="LINUX64" # For Global arrays 4.1b build only
export NWCHEM_MODULES="pnnl"
export USE_MPI="y"
export USE_MPIF="y"
export USE_MPIF4="y"   # Needed for 32-bit integer builds.
#export OMPI_F77="gfortran"
#export OMPI_FC="gfortran"
#export LIBMPI="-lmpich -lmpichf90" # MPICH-2
export LIBMPI="-lmpi_f90 -lmpi_f77 -lmpi -lopen-rte -lopen-pal -lnsl -lm"
#export MPI_LIB=/path/to/MPIlibs
#export MPI_INCLUDE=/path/to/MPIheaders
export ARMCI_DEFAULT_SHMMAX=4196
export ARMCI_NETWORK="OPENIB"
export IB_HOME="/usr" #Verify location on Peregrine
export IB_INCLUDE="$IB_HOME/include"
export IB_LIB="$IB_HOME/lib64"
export IB_LIB_NAME="-libverbs"
export HAS_BLAS="yes"
export USE_64TO32="y"
export BLASOPT=$BLASLIB
#export BLAS_LIB="-L/copt/2.0/ATLAS/3.8.1/lib64 -lptf77blas -latlas" # For Global arrays build only
export PYTHONHOME="/fix for peregrines/python/Python-2.7"
export PYTHONVERSION="2.7"  #Fix for peregrine
#   1) cd $NWCHEM_TOP/src
#   2) make clean
#   3) make 64_to_32
#   4) make nwchem_config
#   4) make

