#pragma once
#include "counters.hpp"
#include <iostream>

class LinkedList {
private:
    struct Node {
        int data;
        Node *next;

        Node(int v) : data(v), next(nullptr) {}
    };

    Node *head;
    mutable Counters c{};

public:
    LinkedList() : head(nullptr) {}

    ~LinkedList() {
        Node *curr = head;

        while (curr) {
            Node *temp = curr;
            curr = curr->next;
            // structural_ops++
            c.structural_ops++;
            delete temp;
        }
    }

     void runJobFile(std::string fname)
    {
        std::ifstream f(fname);
        json j = json::parse(f);
        // std::cout<<j<<std::endl;


        for (auto &element : j)
        {  
            // Parses json for the key value which indicates the operation
            // and the value which holds the integer that is being operated on
            std::string op = element["op"];
            int val = element["value"];

            if (op == "contains") {
                contains(val);
            } else if (op == "insert") {
                insert(val);
            } else if (op == "delete") {
                erase(val);
            }

        }
    }

    bool insert(int value) {
        // inserts++
        c.inserts++;

        if (contains(value))
            return false;

        Node *n = new Node(value);
        n->next = head;
        head = n;
        // structural_ops++
        c.structural_ops++;

        return true;
    }

    bool contains(int value) const {
        // lookups++
        c.lookups++;

        Node *curr = head;

        while (curr) {
            // comparison++
            c.comparisons++;
            if (curr->data == value)
                return true;

            curr = curr->next;
        }

        // comparison++ (for the final nullptr check that exits the loop)
        c.comparisons++;
        return false;
    }

    bool erase(int value) {
        // deletes++
        c.deletes++;

        Node *curr = head;
        Node *prev = nullptr;

        while (curr) {
            // comparison++
            c.comparisons++;
            if (curr->data == value) {

                if (prev)
                    prev->next = curr->next;
                else
                    head = curr->next;

                // structural_ops++
                c.structural_ops++;
                delete curr;
                return true;
            }

            prev = curr;
            curr = curr->next;
        }

        // comparison++ (for the final nullptr check that exits the loop)
        c.comparisons++;
        return false;
    }

    void print() const {
        Node *curr = head;

        while (curr) {
            std::cout << curr->data << " ";
            curr = curr->next;
        }

        std::cout << "\n";
    }

    Counters getCounters() {
        return c;
    }

    void save(std::string filename, bool dict = true) {
        c.saveCounters(filename, dict);
    }

    void reset() {
        c = {};
        Node *curr = head;
        while (curr) {
            Node *temp = curr;
            curr = curr->next;
            delete temp;
        }
        head = nullptr;
    }

    virtual const char *name() const {
        return "LinkedList";
    }
};