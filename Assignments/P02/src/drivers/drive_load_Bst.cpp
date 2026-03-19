#include "bst.hpp"
#include <iostream>
#include <string>

using namespace std;

int main(int argc,char**argv) {
    Bst tree;

    // if(argc < 2){
    //     cout<<"Error: You need a filename!"<<endl;
    //     cout<<"Usage: ./dbst ../work_files/workload_A_1000.json"<<endl;
    // }

    Counters counter = tree.getCounters();

    for (int i = 0; i<100; i++){
        tree.insert(rand());
    }
    cout << counter << endl;

    cout << "Reseting Counters and Binary Search Tree..." << endl;
    tree.reset();
    cout << counter << endl;


    // tree.runJobFile(argv[1]);
    
}