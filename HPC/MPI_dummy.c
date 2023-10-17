/* File to create MPI context for, e.g., reporting of rank mapping by MPI library.
Does not do anything. */

#include <stdio.h>
#include <unistd.h>
#include <mpi.h>

int main (int argc, char** argv)
{
  int rank, size;
  MPI_Init (&argc, &argv);      /* starts MPI */
  MPI_Comm_rank (MPI_COMM_WORLD, &rank);        /* get current process id */
  MPI_Comm_size (MPI_COMM_WORLD, &size);        /* get number of processes */
  MPI_Finalize();
  return 0;
}
