#include "sortedArraySet.hpp"
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char** argv) {
    // We now expect: ./dlinkedlist <input_file> <output_results_file>
    if (argc < 3) {
        cout << "Error: Missing arguments!" << endl;
        cout << "Usage: ./dsortedarray <workload.json> <results.json>" << endl;
        return 1;
    }

    SortedArraySet sArrary;
    string input_file = argv[1];
    string output_file = argv[2];

    // 1. Process the specific workload file
    sArrary.runJobFile(input_file);

    // 2. Output the final counters to the console for a quick check
    cout << "Finished " << input_file << " -> " << sArrary.getCounters() << endl;

    // 3. Save the results to the unique filename provided
    // dict=true saves as a dictionary with named keys
    sArrary.save(output_file, true);

    return 0;
}