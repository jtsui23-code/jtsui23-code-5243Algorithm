#pragma once

#include "counters.hpp"
#include "json.hpp"
#include <cstddef>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using json = nlohmann::json;

class HashTable {
private:
    std::vector<std::vector<int>> table;
    std::size_t capacity;
    mutable Counters c{};

    // Integer hash function
    std::size_t hash(int key) const {
        return static_cast<std::size_t>(key) * 2654435761u;
    }

    // Compress hash value into a valid bucket index
    std::size_t indexFor(int key) const {
        return hash(key) % capacity;
    }

public:
    explicit HashTable(std::size_t cap = 101)
        : table(cap), capacity(cap) {}

    bool insert(int key) {
        // inserts++
        c.inserts++;

        std::size_t idx = indexFor(key);
        auto &bucket = table[idx];

        // Check for duplicates
        for (int value : bucket) {
            // comparison++
            c.comparisons++;
            if (value == key) {
                return false;
            }
        }

        // structural_ops++
        c.structural_ops++;
        bucket.push_back(key);
        return true;
    }

    bool contains(int key) const {
        // lookups++
        c.lookups++;

        std::size_t idx = indexFor(key);
        const auto &bucket = table[idx];

        for (int value : bucket) {
            // comparison++
            c.comparisons++;
            if (value == key) {
                return true;
            }
        }

        // comparison++ (final miss check)
        c.comparisons++;
        return false;
    }

    bool erase(int key) {
        // deletes++
        c.deletes++;

        std::size_t idx = indexFor(key);
        auto &bucket = table[idx];

        for (std::size_t i = 0; i < bucket.size(); i++) {
            // comparison++
            c.comparisons++;
            if (bucket[i] == key) {
                // swap-pop delete: fast, order not preserved
                // structural_ops++
                c.structural_ops++;
                bucket[i] = bucket.back();
                bucket.pop_back();
                return true;
            }
        }

        // comparison++ (final miss check)
        c.comparisons++;
        return false;
    }

    void runJobFile(std::string fname) {
        std::ifstream f(fname);
        json j = json::parse(f);

        for (auto &element : j) {
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

    Counters getCounters() const {
        return c;
    }

    void save(std::string filename, bool dict = true) {
        c.saveCounters(filename, dict);
    }

    void reset() {
        c = {};
        for (auto &bucket : table) {
            bucket.clear();
        }
    }

    const char *name() const {
        return "HashTable";
    }
};