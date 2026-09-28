import subprocess, os

with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f"Total lines in script_3.js: {total}")

# We check chunks of increasing size from 1 to total lines
for n in range(500, total, 250):
    chunk = "".join(lines[:n])
    with open('scratch/temp_check.js', 'w', encoding='utf-8') as tf:
        tf.write(chunk)
    res = subprocess.run(['node', '--check', 'scratch/temp_check.js'], capture_output=True, text=True)
    if "Unexpected end of input" not in res.stderr and res.returncode != 0:
        print(f"Syntax error introduced at or before line {n}:")
        print(res.stderr)
        break

# Now do fine search around line total
print("Checking full script...")
res = subprocess.run(['node', '--check', 'scratch/script_3.js'], capture_output=True, text=True)
print("Full script error:")
print(res.stderr)
