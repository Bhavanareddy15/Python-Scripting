from pathlib import Path

file_path = Path(__file__).parent/"log_file.txt"

log = {}

with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        date = parts[0]
        type = parts[1]
        if date not in log:
            log[date] = {}
        if type not in log[date]:
            log[date][type] = 0
        
        log[date][type] += 1

for date in log:
    print(f'{date} -> {log[date]}')



