#include <fstream> 
#include <iostream>

using namespace std;

int main()
{
	ofstream outfile;
    outfile.open("./result.txt", ios::app);
    outfile << "aadfeerere" << "\t" << "r548e8824" << "\t" << endl;
    outfile.close();

}
