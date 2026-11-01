import re

with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

results = []
for i, line in enumerate(lines):
    if '33plus' in line.lower() or '34plus' in line.lower():
        # filter out CSS variables like --color-34plus or --color-33plus
        if '--color-33plus' in line or '--color-34plus' in line:
            continue
        results.append(f"{i+1}: {line.strip()[:110]}")

with open('scratch/33plus_matches.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(results))

print(f"Found {len(results)} matches written to scratch/33plus_matches.txt")
