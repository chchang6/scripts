#include <stdlib.h>
#include <stdio.h>

char nodeid[8];
char semdata[2048];
FILE* nodeid_file;
FILE* semdata_file;

int main()
{
 if ( (nodeid_file = popen("uname -n", "r")) == NULL)
  { perror("Execute uname"); }
 if (fgets(nodeid, sizeof(nodeid), nodeid_file) == NULL)
  {
   perror("Got node name");
  }
 printf("My node name is %8s\n", nodeid);
 pclose(nodeid_file);
 semdata_file = popen("ipcs -a", "r");
 //if ( (semdata_file = popen("ipcs -a", "r")) == NULL)
 // { perror("Execute ipcs"); }
 fgets(semdata, 1024, semdata_file);
 /*if (fgets(semdata, 1024, semdata_file) == NULL)
  {
   perror("Got semdata");
  }*/
 printf("Semaphore data\n");
 printf("%s", semdata);
 pclose(semdata_file);
 return 0;
}

