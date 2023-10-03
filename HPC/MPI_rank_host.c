#include <stdio.h>
#include <unistd.h>
#include <mpi.h>

int main (int argc, char** argv)
{
  int rank, size;
  char hname[64];

  MPI_Init (&argc, &argv);	/* starts MPI */
  MPI_Comm_rank (MPI_COMM_WORLD, &rank);	/* get current process id */
  MPI_Comm_size (MPI_COMM_WORLD, &size);	/* get number of processes */
  gethostname(hname, sizeof hname);
  printf( "Hello world from process %d of %d on host %s\n", rank, size, hname );
  //printf("My hostname: %s\n", hname);
  MPI_Finalize();
  return 0;
}
