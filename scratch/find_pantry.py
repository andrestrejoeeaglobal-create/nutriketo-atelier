import re

with open('generate_standalone_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

fn_matches = re.findall(r'function\s+([a-zA-Z0-9_]*pantry[a-zA-Z0-9_]*)', text, re.I)
print('Functions:', set(fn_matches))

id_matches = re.findall(r'id=["\']([^"\']*pantry[^"\']*)["\']', text, re.I)
print('IDs:', set(id_matches))

# Find lines where PANTRY_STOCK_INVENTORY is looped or used in rendering
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'PANTRY_STOCK_INVENTORY' in line:
        print(f'{i+1}: {line.strip()[:100]}')
