#!/bin/bash

# Ensure the driver is compiled first
g++ -std=c++20 -Iinclude drivers/drive_load_Bst.cpp -o dbst

# Create a folder for results if it doesn't exist
mkdir -p results

# Arrays of your workload types and sizes
TYPES=("A" "B" "C" "D")
SIZES=(1000 5000 10000 20000)

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

echo "All tests complete. Check the 'results' folder."