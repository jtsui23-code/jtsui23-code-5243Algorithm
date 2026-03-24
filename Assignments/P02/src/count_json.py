import json
import glob
import os

# 1. Get the directory where the script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Point to the work_files folder
data_folder = os.path.join(script_dir, "work_files")

# 3. Find and sort files
search_pattern = os.path.join(data_folder, "workload_*.json")
files = sorted(glob.glob(search_pattern))

# Print a clean header
print(f"\n{'JSON Filename':<25} | {'Element Count':>12}")
print("-" * 40)

for filepath in files:
    try:
        # os.path.basename removes the "C:/Users/.../work_files/" part
        filename_only = os.path.basename(filepath)
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            
            if isinstance(data, list):
                count = len(data)
                # :<25 aligns text left, :>12 aligns numbers right with commas
                print(f"{filename_only:<25} | {count:>12,}")
            else:
                print(f"{filename_only:<25} | Not a list")
                
    except Exception as e:
        # Using basename here too so errors are readable
        short_name = os.path.basename(filepath)
        print(f"Error reading {short_name}: {e}")

print("-" * 40)