#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
   int mem = 1024*1024*sizeof(int);
   char* ptr = malloc(mem);
   memset(ptr, 0, mem);
   sleep(60);
   free(ptr);
}

