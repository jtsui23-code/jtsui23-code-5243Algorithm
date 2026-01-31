/*****************************************************************************
*                    
*  Author:           Jack Tsui
*  Email:            jtsui1110@my.msutexas.edu
*  Label:            P01
*  Title:            BST Delete
*  Course:           5243 Algorithm Analysis
*  Semester:         Spring 2026
* 
*  Description:
*        This program shows implementation of the delete function of a node from a Binary Search Tree (BST).
* 
*  Usage:
*       g++ Jackbst.cpp -o JackBST.exe
*      ./[EXECUTABLE] 
* 
*  Files:            
*                    JackTsuibst.cpp
*                    bst.exe 
*                    
*
*****************************************************************************/
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

struct Node {
    int data;
    Node *left;
    Node *right;

    Node(int x) {
        data = x;
        left = right = nullptr;
    }
};

class GraphvizBST {
public:
    static void saveDotFile(const std::string &filename, const std::string &dotContent) {
        std::ofstream outFile(filename);
        if (outFile.is_open()) {
            outFile << dotContent;
            outFile.close();
            std::cout << "DOT file saved: " << filename << std::endl;
        } else {
            std::cerr << "Error: Could not open file " << filename << std::endl;
        }
    }

    static std::string generateDot(const Node *root) {
        std::string dot = "digraph BST {\n";
        dot += "    node [fontname=\"Arial\"];\n";
        dot += generateDotHelper(root);
        dot += "}\n";
        return dot;
    }

private:
    static std::string generateDotHelper(const Node *node) {
        if (!node)
            return "";
        std::string result;
        if (node->left) {
            result += "    " + std::to_string(node->data) + " -> " + std::to_string(node->left->data) + " [label=\"L\"];\n";
            result += generateDotHelper(node->left);
        } else {
            std::string nullNode = "nullL" + std::to_string(node->data);
            result += "    " + nullNode + " [shape=point];\n";
            result += "    " + std::to_string(node->data) + " -> " + nullNode + ";\n";
        }
        if (node->right) {
            result += "    " + std::to_string(node->data) + " -> " + std::to_string(node->right->data) + " [label=\"R\"];\n";
            result += generateDotHelper(node->right);
        } else {
            std::string nullNode = "nullR" + std::to_string(node->data);
            result += "    " + nullNode + " [shape=point];\n";
            result += "    " + std::to_string(node->data) + " -> " + nullNode + ";\n";
        }
        return result;
    }
};

class Bst {
    Node *root;

    void _print(Node *subroot) {
        if (!subroot) {
            return;
        } else {
            _print(subroot->left);
            cout << subroot->data << " ";
            _print(subroot->right);
        }
    }
    void _insert(Node *&subroot, int x) {
        if (!subroot) { // if(root == nullptr)
            subroot = new Node(x);
        } else {
            if (x < subroot->data) {
                _insert(subroot->left, x);
            } else {
                _insert(subroot->right, x);
            }
        }
    }
    int _ipl(Node *root, int depth = 0) {
        if (!root)
            return 0; // Base case: Empty subtree contributes 0 to IPL
        return depth + _ipl(root->left, depth + 1) + _ipl(root->right, depth + 1);
    }


    // Part of Delete function rest is in Public with a function called deleteNode(int x)
    // -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    /**
     * Private: _findMin
     * * Description:
     *      Traverses to the leftmost node of a given subtree to find the
     *      minimum value.
     * 
     * * Parameters:
     *      - Node* node: The starting node for the search.
     * 
     * * Returns:
     *      - Node*: A pointer to the node containing the minimum value.
     */
    Node* _findMin(Node* subroot) {
        while (subroot && subroot->left) {
            subroot = subroot->left;
        }
        return subroot;
    }


    /**
     * Private: _delete
     * Description:
     *      Recursively searches for a node with the specified value and removes it.
     *      Handles three cases: leaf nodes, nodes with one child, and nodes with 
     *      two children using the inorder successor (smallest in right subtree).
     * 
     * * Parameters:
     *      - Node* &subroot: Reference to the current node pointer being evaluated.
     *      - int x: The integer value to be removed from the tree.
     * 
     * * Returns:
     * -     void: Modifies the tree in place via pointer reference.
     * 
     */
    void _delete(Node*& subroot, int x) {
        if (!subroot) {
            return; // Value not found
        }
        
        if (x < subroot->data) {
            // Value is in left subtree
            _delete(subroot->left, x);
        } 
        else if (x > subroot->data) {
            // Value is in right subtree
            _delete(subroot->right, x);
        } 
        else {
            // Found the node to delete
            
            // Case 1: Node with no children or one child
            if (!subroot->left) {
                Node* temp = subroot;
                subroot = subroot->right;
                delete temp;
            }
            else if (!subroot->right) {
                Node* temp = subroot;
                subroot = subroot->left;
                delete temp;
            }
            // Case 2: Node with two children
            else {
                // Find in-order successor (smallest in right subtree)
                Node* successor = _findMin(subroot->right);
                
                // Copy successor's data to this node
                subroot->data = successor->data;
                
                // Delete the successor
                _delete(subroot->right, successor->data);
            }
        }
    }


    // -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

public:




    Bst() { root = nullptr; }
    void insert(int x) { _insert(root, x); }
    bool search(int key) { return 0; }
    void print() { _print(root); }
    void saveDotFile(const std::string &filename) {
        std::string dotContent = GraphvizBST::generateDot(root);
        GraphvizBST::saveDotFile(filename, dotContent);
    }

    /**
     * Computes the Internal Path Length (IPL) of a Binary Search Tree (BST).
     *
     * Definition:
     * The Internal Path Length (IPL) of a BST is the sum of the depths of all nodes in the tree.
     * The depth of a node is the number of edges from the root to that node.
     *
     * Example:
     *        10
     *       /  \
     *      5    15
     *     / \     \
     *    2   7    20
     *
     * IPL = (depth of 10) + (depth of 5) + (depth of 15) + (depth of 2) + (depth of 7) + (depth of 20)
     *     = 0 + 1 + 1 + 2 + 2 + 2 = 8
     *
     * @param root Pointer to the root node of the BST.
     * @param depth Current depth of the node (default is 0 for the root call).
     * @return The sum of depths of all nodes (Internal Path Length).
     */
    int ipl() {
        return _ipl(root);
    }


    /**
     * Public: remove
     * * Description:
     *      Public method to remove a value from the BST.
     * 
     * * Parameters:
     *      - int x: The value to be removed.
     * 
     * * Returns:
     * - void
     */
    void remove(int x) {
            _delete(root, x);
        }

};

bool unique_value(int *arr, int n, int x) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == x) {
            return false;
        }
    }
    return true;
}

int main() {
    // Bst tree;
    // int root = pow(2, 15) / 2;
    // int max = pow(2, 15) - 1;
    // vector<int> arr;
    // arr.push_back(root);
    // tree.insert(root);
    // for (int i = 1; i < 5000; i++) {
    //     int r = rand() % max;
    //     while (!unique_value(arr.data(), arr.size(), r)) {
    //         r = rand() % max;
    //     }
    //     tree.insert(r);
    //     arr.push_back(r);
    // }

    // tree.print();
    // tree.saveDotFile("bst_snapshot.dot");

    // Bst tree2;
    // tree2.insert(10);
    // tree2.insert(5);
    // tree2.insert(15);
    // tree2.insert(2);
    // tree2.insert(7);
    // tree2.insert(20);
    // cout << "Internal Path Length: " << tree2.ipl() << endl;



    Bst testTree;
    testTree.insert(5);
    testTree.insert(25);
    testTree.insert(52);
    testTree.insert(21);
    testTree.insert(33);
    testTree.insert(62);
    testTree.insert(1083);
    testTree.insert(23874);


    cout << "Before deletion: ";
    testTree.print();
    cout << endl;

    testTree.remove(21); 
    testTree.remove(25);  
    testTree.remove(5);  

    cout << "After deletion: ";
    testTree.print();
    cout << endl;
}
