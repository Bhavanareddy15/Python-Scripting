
import os

from pathlib import Path

# Build path relative to the script file itself
#script_dir = os.path.dirname(os.path.abspath(__file__))
#file_path = os.path.join(script_dir, "result.txt")

file_path = Path(__file__).parent / "result.txt"

log = {}

with open(file_path, "r") as file:
    for line in file:
        parts = line.split()
        
        if not parts:
            continue

        status = parts[0] 
        error = int(parts[1]) if (len(parts)>1) else None

        if error is None:
            if status not in log:
                log[status] = 0
            log[status] += 1  

        else:
            if status not in log:
                log[status] = {}
            if error not in log[status]:
                log[status][error] = 0  
            log[status][error] += 1

print(log)
print(f'Pass: {log['PASS']}')




