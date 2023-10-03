#include <sys/time.h>
#include <sys/resource.h>
#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

main(int argc, char* argv[]) {
   int my_rank;
   int total_ranks;
   unsigned int soft_VM_limit_MB, hard_VM_limit_MB;
   char host[512];
   struct rlimit VM_limit;
   host[511] = '\0';
   MPI_Init(&argc, &argv);
   MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
   MPI_Comm_size(MPI_COMM_WORLD, &total_ranks);
   gethostname(host, 511);
   getrlimit(RLIMIT_AS, &VM_limit);
   soft_VM_limit_MB = VM_limit.rlim_cur/1024/1024;
   hard_VM_limit_MB = VM_limit.rlim_max/1024/1024;
   printf("Rank %i of %i on host %s has a soft limit of %u MB and a hard limit of %u MB\n", my_rank, total_ranks, host, 
      soft_VM_limit_MB, hard_VM_limit_MB);
   MPI_Finalize();
   exit(0);
}
