#include "bst.hpp"
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char** argv) {
    // We now expect: ./dbst <input_file> <output_results_file>
    if (argc < 3) {
        cout << "Error: Missing arguments!" << endl;
        cout << "Usage: ./dbst <workload.json> <results.json>" << endl;
        return 1;
    }

    Bst tree;
    string input_file = argv[1];
    string output_file = argv[2];

    // 1. Process the specific workload file
    tree.runJobFile(input_file);

    // 2. Output the final counters to the console for a quick check
    cout << "Finished " << input_file << " -> " << tree.getCounters() << endl;

    // 3. Save the results to the unique filename provided
    // dict=false saves as an array: [comp, ops, ins, del, look, res]
    tree.save(output_file, true); 

    return 0;
}