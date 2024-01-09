#include <stdlib.h>
#include <iostream>
#include <string>
#include <cstdio>
#include <sstream>
#include <fstream>

#include "libsnark/common/default_types/r1cs_ppzksnark_pp.hpp"

using namespace libsnark;
using namespace std;
using std::string;
using std::endl;

bool isNumber(const string& str)
{
    for (char const &c : str) {
        if (std::isdigit(c) == 0) return false;
    }
    return true;
}

int main(int argc, char *argv[])
{
  typedef libff::Fr<default_r1cs_ppzksnark_pp> FieldT;

  // Initialize the curve parameters
  default_r1cs_ppzksnark_pp::init_public_params();
  
  FieldT tmp = FieldT::one();

  unsigned long data1;
  unsigned long data2;
  unsigned long data3;
  unsigned long data4;

  if (isNumber(argv[1])){
    if (argc == 5){
      data1 = std::stoul(argv[1]);
      data2 = std::stoul(argv[2]);
      data3 = std::stoul(argv[3]);
      data4 = std::stoul(argv[4]);

      tmp.mont_repr.data[0] = data1;
      tmp.mont_repr.data[1] = data2;
      tmp.mont_repr.data[2] = data3;
      tmp.mont_repr.data[3] = data4;

      std::cout << tmp;
    }
    else if (argc == 6){
      throw std::invalid_argument("Currently doesn't support 5 numbers montgomery representative.");
    }
    else{
      throw std::invalid_argument("Invalid number of stdin arguments");
    }
  }
  else if (!isNumber(argv[1])){
    if (argc == 3){
      std::ifstream infile(argv[1]);
      ofstream outfile(argv[2]);
      std::string line;

      int outfirst = 1;
      
      while (std::getline(infile, line))
      {
          std::istringstream iss(line);

          if (!(iss >> data1 >> data2 >> data3 >> data4))
          {
            outfile.close();
            break;
          }

          tmp.mont_repr.data[0] = data1;
          tmp.mont_repr.data[1] = data2;
          tmp.mont_repr.data[2] = data3;
          tmp.mont_repr.data[3] = data4;
          
          if (outfirst){
            outfirst = 0;
            outfile << tmp;
          }
          else{
            outfile << endl << tmp;
          }
      }
    }
    else{
      throw std::invalid_argument("Invalid number of stdin arguments");
    }
  }

  return 0;
}
