// Script to test ability to limit memory on single process.
// Expectation to use with PBS script and e.g., -l mem or ulimit
// 2 GB = 536870912 32-bit integers = 2097152 kB
int main() {
   int testarray[536870912] = { 0 }; // Does not build with 2GB process limit
   int testarray[536870911] = { 0 }; // Builds OK with 2GB process limit
   int size_testarray = sizeof(testarray);
   printf("Size of allocated test array = %u bytes\n", size_testarray);
}

