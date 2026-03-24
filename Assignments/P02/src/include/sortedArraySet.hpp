#pragma once

#include "counters.hpp"
#include "json.hpp"
#include <cstddef>
#include <fstream>
#include <iostream>
#include <string>

using json = nlohmann::json;

class SortedArraySet {
private:
    int *data;
    std::size_t count;
    std::size_t capacity;
    mutable Counters c{};

    void resize(std::size_t newCapacity) {
        int *newData = new int[newCapacity];

        for (std::size_t i = 0; i < count; i++) {
            // structural_ops++ (copying each element over)
            c.structural_ops++;
            newData[i] = data[i];
        }

        delete[] data;
        data = newData;
        capacity = newCapacity;

        // resize_events++
        c.resize_events++;
    }

    // Returns the index where value is found,
    // or where it should be inserted to maintain sorted order.
    std::size_t lowerBound(int value) const {
        std::size_t left = 0;
        std::size_t right = count;

        while (left < right) {
            std::size_t mid = left + (right - left) / 2;

            // comparison++
            c.comparisons++;
            if (data[mid] < value) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

public:
    explicit SortedArraySet(std::size_t initialCapacity = 8)
        : data(new int[initialCapacity]), count(0), capacity(initialCapacity) {}

    ~SortedArraySet() {
        delete[] data;
    }

    std::size_t size() const {
        return count;
    }

    bool empty() const {
        return count == 0;
    }

    bool contains(int value) const {
        // lookups++
        c.lookups++;

        if (count == 0) {
            // comparison++
            c.comparisons++;
            return false;
        }

        std::size_t pos = lowerBound(value);

        // comparison++ (final check: is what we found actually the value?)
        c.comparisons++;
        return pos < count && data[pos] == value;
    }

    bool insert(int value) {
        // inserts++
        c.inserts++;

        std::size_t pos = lowerBound(value);

        // comparison++ (duplicate guard)
        c.comparisons++;
        if (pos < count && data[pos] == value) {
            return false;
        }

        // Grow array if full
        if (count == capacity) {
            resize(capacity * 2);
        }

        // Shift elements right to make room
        for (std::size_t i = count; i > pos; i--) {
            // structural_ops++
            c.structural_ops++;
            data[i] = data[i - 1];
        }

        // structural_ops++ (placing the new value)
        c.structural_ops++;
        data[pos] = value;
        count++;

        return true;
    }

    bool erase(int value) {
        // deletes++
        c.deletes++;

        if (count == 0) {
            // comparison++
            c.comparisons++;
            return false;
        }

        std::size_t pos = lowerBound(value);

        // comparison++ (did we actually find the value?)
        c.comparisons++;
        if (pos >= count || data[pos] != value) {
            return false;
        }

        // Eager delete: shift everything left to close the gap
        for (std::size_t i = pos; i + 1 < count; i++) {
            // structural_ops++
            c.structural_ops++;
            data[i] = data[i + 1];
        }

        count--;
        return true;
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
        count = 0;
    }

    const char *name() const {
        return "SortedArraySet";
    }

    void print() const {
        std::cout << "[";
        for (std::size_t i = 0; i < count; i++) {
            std::cout << data[i];
            if (i + 1 < count) {
                std::cout << ", ";
            }
        }
        std::cout << "]\n";
    }
};