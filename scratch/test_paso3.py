import json
import re

# Load the 106 items from scratch/test_refined_pairs.py logic
from test_refined_pairs import are_equivalent_v2, item_keywords

with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

pantry_match = re.search(r"window\.PANTRY_STOCK_INVENTORY\s*=\s*(\{[\s\S]*?\n\s*\});", text)
pantry_items = []
for m in re.finditer(r'"(sku-\d+-[^"]+)":\s*\{\s*item_num:\s*(\d+),\s*name:\s*"([^"]+)",\s*stock:\s*([\d\.]+),\s*unit:\s*"([^"]+)",\s*packaging:\s*"([^"]+)",\s*status:\s*"([^"]+)"', pantry_match.group(1)):
    pantry_items.append({
        "sku": m.group(1),
        "item_num": int(m.group(2)),
        "name": m.group(3),
        "stock": float(m.group(4)),
        "unit": m.group(5),
        "packaging": m.group(6),
        "status": m.group(7)
    })

print(f"Total physical SKUs in PANTRY_STOCK_INVENTORY: {len(pantry_items)}")

# Simulate nonFarm list in initSetupPanel
non_farm = []
for p in pantry_items:
    already = any(are_equivalent_v2(existing["name"], p["name"]) for existing in non_farm)
    if not already:
        non_farm.append(p)
    else:
        print(f"WARNING: '{p['name']}' was considered already in list!")

print(f"Total items shown in Paso 3: {len(non_farm)} (Should be exactly 106)")
