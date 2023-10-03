#include <mpi.h>
#include <stdio.h>
#include <unistd.h>
#include <utmpx.h>
#include <sched.h>

int main(int argc, char* argv[]) {
   int i, namelen, rank, size, core_id;
   char name[MPI_MAX_PROCESSOR_NAME];

   MPI_Init(&argc, &argv);
   MPI_Comm_size(MPI_COMM_WORLD, &size);
   MPI_Comm_rank(MPI_COMM_WORLD, &rank);
   MPI_Get_processor_name(name, &namelen);
   core_id = sched_getcpu();

   printf("Rank %d of %d running on core %d, node %s\n", rank, size, core_id, name);
 
   MPI_Finalize();

   return(0);
}

