// Build with g++ -o allocate_lots allocate_lots.cxx
#include <iostream>
#include <vector>
#include <string>
#include <unistd.h>

void foo(int64_t numints) {
   size_t tsize = 0;
   std::vector <int64_t> t (numints);
   tsize = t.size() * sizeof(int64_t) / 1e9;
   std::cout << "Allocated " << tsize << " GB memory" << std::endl;
   sleep(10);
   return;
}
   
int main () {
   std::string input;
   int i;
   std::cout << "How much memory should I allocate in GB? ";
   std::cin >> input;
   i = std::stoi(input);
   foo(i*1e9/sizeof(int64_t));
   return 0;
}


