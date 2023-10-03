#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "mpi.h"
#define intmin(a,b) ( ((a) < (b)) ? (a) : (b) )
// Remember to define NUMFRAMES at compile time.
char frame[5];
//char commandroot[] = "vmd -dispdev text < test.tcl -args ";
char commandroot[] = "vmd -dispdev text < pathways3.tcl -args ";
char command[66];
char commandtail[] = " | sed '/^[^CPR]/d'";
int i; //i is general dummy counter
int framearray[NUMFRAMES+1];
int wstatus = 1, toworkframe = 0;
char **argv;
int argc, sender, numprocs, myid; // MPI variables
MPI_Status status;
int *worker_status; // Boss check and worker report status buffers
int *tosendframe = NULL;// Boss send and worker receive frame buffers
int main()
{
 MPI_Init(&argc, &argv);
 MPI_Comm_size(MPI_COMM_WORLD, &numprocs);
 MPI_Comm_rank(MPI_COMM_WORLD, &myid);
 if (myid == 0)
 {
  // First fill frame array with frame values to send.
  tosendframe = framearray;
  for (i = 0; i <= NUMFRAMES; i++)
  {
   *tosendframe = i;
   ++tosendframe;
  } 
  // Initialize pointer to start of array.
  tosendframe = framearray;
  // Now send off first numprocs jobs 
  for (i = 1; i < intmin(NUMFRAMES,numprocs); ++i)
  {
   MPI_Send(tosendframe, 1, MPI_INT, i, 1, MPI_COMM_WORLD);
   printf("Sent frame %i to rank %i\n",*tosendframe,i);
   ++tosendframe;
  }
  // Now send one off each time one is received until tosendframe points at last entry.
  // Since interesting output is created on worker processes, don't have to receive anything
  // after that.
  worker_status=&wstatus;
  for (i = 0; i < NUMFRAMES; i++)
  {
   MPI_Recv(worker_status, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
   sender = status.MPI_SOURCE;
   if (*tosendframe < NUMFRAMES)
   {
    MPI_Send(tosendframe, 1, MPI_INT, sender, 1, MPI_COMM_WORLD);
    printf("Sent frame %i to rank %i\n", *tosendframe, sender);
    ++tosendframe;
   }
   else // Worker kill
   {
    MPI_Send(tosendframe, 1, MPI_INT, sender, 1, MPI_COMM_WORLD);
   }
  }
  printf("Rank 0 is done.\n");
 }
 else // Worker processes
 {
  if (myid > NUMFRAMES)
  {//Someone has requested more processes than frames. Don't do anything
   printf("Here I should not be.\n");
  }
  else
  {//Work
   while (1)
   {
    MPI_Recv(&toworkframe, 1, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status); 
    if (toworkframe == NUMFRAMES)
    {
     break;
    }
    printf("Rank %i got frame %i\n", myid, toworkframe);
    strcpy(command, commandroot);
    snprintf(frame, 5, "%-5i", toworkframe);
    strcat(command, frame);
    strcat(command, commandtail);
    if ( system(command) == 0 )
    {
     printf("Rank %i has completed frame %i\n", myid, toworkframe);
     MPI_Send(&toworkframe, 1, MPI_INTEGER, 0, 0, MPI_COMM_WORLD);
     printf("Rank %i sending frame %i status back to rank 0\n", myid, toworkframe);
    }
   }
   printf("Rank %i is done.\n", myid);
  }
 }
 MPI_Barrier(MPI_COMM_WORLD);
 MPI_Finalize();
 return 0;
}
