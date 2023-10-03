#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "mpi.h"

//char semclear[] = "ipcrm -s SEMID";

int wstatus = 1, toworkframe = 0;
char **argv;
FILE* semaphore_data_file;
char nodeid[8];
char semaphore_data[1024];
int argc, sender, numprocs, myid; // MPI variables
MPI_Status status;
int *worker_status; // Boss check and worker report status buffers

int main()
{
 MPI_Init(&argc, &argv);
 MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
 MPI_Comm_rank(MPI_COMM_WORLD, &myid);
 FILE* nodeid_file = popen("uname -n", "r");
 if (fgets(nodeid, sizeof(nodeid), nodeid_file) == NULL)
  {
   perror("Get node id");
  }
 semaphore_data_file = popen("ipcs -a", "r");
 if (fgets(semaphore_data, sizeof(semaphore_data), semaphore_data_file) == NULL)
 {
  perror("Get semaphore data");
 }
 printf("Rank %i on node %8s shows semaphore data\n", myid, nodeid);
 puts(semaphore_data);
 pclose(nodeid_file);
 pclose(semaphore_data_file);
 MPI_Barrier(MPI_COMM_WORLD);
 MPI_Finalize();
 return 0;
}
