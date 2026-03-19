#!/bin/bash

# Define the workloads and sizes based on your generated files
WORKLOADS=("A" "B" "C" "D")
SIZES=(1000 5000 10000 20000)

# Loop through each combination
for W in "${WORKLOADS[@]}"; do
    for N in "${SIZES[@]}"; do
        FILE="work_files/workload_${W}_${N}.json"
        
        # Check if the file exists before running
        if [ -f "$FILE" ]; then
            echo "-------------------------------------------"
            echo "Running Workload $W with Size $N..."
            ./dbst "$FILE"
        else
            echo "Skipping $FILE: File not found."
        fi
    done
done