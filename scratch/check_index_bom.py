import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const ACTIVE_WEEK_40_CANONICAL_BOM = (\[.*?\]);', html, re.DOTALL)
bom = json.loads(m.group(1))

for it in bom:
    if any(k in it['name'].lower() for k in ['oliva', 'vevo', 'ajonjol', 'mantequilla', 'ghee', 'queso', 'crema']):
        print(f"{it['category']:30} | {it['name']:40} | {it['quantity']} {it['unit']}")
