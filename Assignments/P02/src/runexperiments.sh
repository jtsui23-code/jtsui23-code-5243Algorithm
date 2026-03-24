#!/bin/bash

# Compile all drivers
echo "Compiling drivers..."
g++ -std=c++20 -Iinclude drivers/drive_load_Bst.cpp -o dbst
g++ -std=c++20 -Iinclude drivers/drive_load_LinkedList.cpp -o dlinkedlist
g++ -std=c++20 -Iinclude drivers/drive_load_Hashtable.cpp -o dhashtable
g++ -std=c++20 -Iinclude drivers/drive_load_Sortedarray.cpp -o dsortedarray

# Create a folder for results if it doesn't exist
mkdir -p results

# Arrays of your workload types and sizes
TYPES=("A" "B" "C" "D")
SIZES=(1000 5000 10000 20000)

echo ""
echo "--- Running BST Tests ---"
for T in "${TYPES[@]}"; do
    for S in "${SIZES[@]}"; do
        INPUT="work_files/workload_${T}_${S}.json"
        OUTPUT="results/bst_results_${T}_${S}.json"

        if [ -f "$INPUT" ]; then
            echo "Processing $INPUT..."
            ./dbst "$INPUT" "$OUTPUT"
        else
            echo "Skip: $INPUT not found."
        fi
    done
done

echo ""
echo "--- Running LinkedList Tests ---"
for T in "${TYPES[@]}"; do
    for S in "${SIZES[@]}"; do
        INPUT="work_files/workload_${T}_${S}.json"
        OUTPUT="results/linkedlist_results_${T}_${S}.json"

        if [ -f "$INPUT" ]; then
            echo "Processing $INPUT..."
            ./dlinkedlist "$INPUT" "$OUTPUT"
        else
            echo "Skip: $INPUT not found."
        fi
    done
done

echo ""
echo "--- Running HashTable Tests ---"
for T in "${TYPES[@]}"; do
    for S in "${SIZES[@]}"; do
        INPUT="work_files/workload_${T}_${S}.json"
        OUTPUT="results/hashtable_results_${T}_${S}.json"

        if [ -f "$INPUT" ]; then
            echo "Processing $INPUT..."
            ./dhashtable "$INPUT" "$OUTPUT"
        else
            echo "Skip: $INPUT not found."
        fi
    done
done

echo ""
echo "--- Running SortedArray Tests ---"
for T in "${TYPES[@]}"; do
    for S in "${SIZES[@]}"; do
        INPUT="work_files/workload_${T}_${S}.json"
        OUTPUT="results/sortedarray_results_${T}_${S}.json"

        if [ -f "$INPUT" ]; then
            echo "Processing $INPUT..."
            ./dsortedarray "$INPUT" "$OUTPUT"
        else
            echo "Skip: $INPUT not found."
        fi
    done
done

echo ""
echo "All tests complete. Check the 'results' folder."