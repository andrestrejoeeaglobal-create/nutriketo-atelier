with open('scratch/script_3.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# We check bracket balance function by function or block by block
depth = 0
for line_no, line in enumerate(lines, 1):
    old_depth = depth
    for c in line:
        if c == '{': depth += 1
        elif c == '}': depth -= 1
    if 'function ' in line:
        print(f"Line {line_no:4d} (depth {old_depth} -> {depth}): {line.strip()[:60]}")
    if depth < 0:
        print(f"ERROR: depth went below 0 at line {line_no}")

print(f"Final depth: {depth}")
