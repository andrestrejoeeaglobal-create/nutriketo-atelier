import json
import re
import unicodedata

def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
    html_gen = f.read()

# Load week 41
with open("semana_41_master.json", "r", encoding="utf-8") as f:
    s41 = json.load(f)

# Extract PANTRY_STOCK_INVENTORY JSON
pantry_match = re.search(r"window\.PANTRY_STOCK_INVENTORY\s*=\s*(\{[\s\S]*?\n\s*\});", html_gen)
# We can extract the items with regex
pantry_items = {}
if pantry_match:
    for m in re.finditer(r'"(sku-\d+-[^"]+)":\s*\{\s*item_num:\s*(\d+),\s*name:\s*"([^"]+)",\s*stock:\s*([\d\.]+),\s*unit:\s*"([^"]+)",\s*packaging:\s*"([^"]+)",\s*status:\s*"([^"]+)"', pantry_match.group(1)):
        pantry_items[m.group(1)] = {
            "item_num": int(m.group(2)),
            "name": m.group(3),
            "stock": float(m.group(4)),
            "unit": m.group(5),
            "packaging": m.group(6),
            "status": m.group(7)
        }

print(f"Loaded {len(pantry_items)} pantry items from PANTRY_STOCK_INVENTORY.")

# Now extract areInsumosEquivalent rules from generate_standalone_html.py
# Let's inspect the itemKeywords in generate_standalone_html.py
item_keywords_match = re.search(r"const itemKeywords = \[([\s\S]*?)\];", html_gen)
item_keywords = []
if item_keywords_match:
    for m in re.finditer(r"\{\s*stem:\s*'([^']+)',\s*aliases:\s*\[([^\]]+)\](?:,\s*exclude:\s*\[([^\]]+)\])?\s*\}", item_keywords_match.group(1)):
        stem = m.group(1)
        aliases = [a.strip().strip("'\"") for a in m.group(2).split(',')]
        exclude = [e.strip().strip("'\"") for e in m.group(3).split(',')] if m.group(3) else []
        item_keywords.append({
            "stem": stem,
            "aliases": aliases,
            "exclude": exclude
        })

print(f"Loaded {len(item_keywords)} itemKeywords rules.")

# Extract INGREDIENT_CANONICAL_MAP_JS
canonical_map_match = re.search(r"const INGREDIENT_CANONICAL_MAP_JS = \{([\s\S]*?)\};", html_gen)
canonical_map = {}
if canonical_map_match:
    lines = canonical_map_match.group(1).split('\n')
    for l in lines:
        m = re.match(r'\s*"([^"]+)":\s*(\[[^\]]+\])', l)
        if m:
            canonical_map[m.group(1)] = json.loads(m.group(2).replace("'", '"'))

def normalize_slug(raw_name):
    if not raw_name: return ""
    clean = strip_accents(raw_name)
    for slug, aliases in canonical_map.items():
        for alias in aliases:
            a_clean = strip_accents(alias)
            if a_clean in clean or clean in a_clean:
                return slug
    return re.sub(r'[^a-z0-9\s-]', '', clean).replace(' ', '-')

def are_equivalent(a_name, b_name):
    if not a_name or not b_name: return False
    a = strip_accents(a_name).replace("nuex", "nuez")
    b = strip_accents(b_name).replace("nuex", "nuez")
    if a == b: return True

    for entry in item_keywords:
        if entry["exclude"]:
            if any(ex in a for ex in entry["exclude"]) or any(ex in b for ex in entry["exclude"]):
                continue
        a_match = any(alias in a for alias in entry["aliases"])
        b_match = any(alias in b for alias in entry["aliases"])
        if a_match and b_match:
            return True

    slug_a = normalize_slug(a_name)
    slug_b = normalize_slug(b_name)
    if slug_a and slug_b and (slug_a == slug_b or slug_a in slug_b or slug_b in slug_a):
        return True
    return False

# Consolidate Week 41 BOM
bom = []
for day in s41["days"]:
    for meal in day["meals"]:
        for course in ['starter', 'main_dish', 'dessert', 'side_dish', 'side', 'drink', 'main']:
            c = meal.get(course)
            if isinstance(c, dict) and "ingredients" in c:
                for ing in c["ingredients"]:
                    bom.append({
                        "name": ing["name"],
                        "quantity": ing["amount"],
                        "unit": ing.get("unit", ""),
                        "category": ing.get("category", "")
                    })

consolidated = {}
for item in bom:
    key = item["category"] + "___" + item["name"]
    if key not in consolidated:
        consolidated[key] = {**item}
    else:
        consolidated[key]["quantity"] += item["quantity"]

print(f"Total unique consolidated ingredients: {len(consolidated)}")

harvest_list = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"]

results = []
for key, item in consolidated.items():
    name = item["name"]
    qty = item["quantity"]
    unit = item["unit"]
    cat = item["category"]

    is_harvest = any(are_equivalent(h, name) for h in harvest_list) or "Cosecha" in cat
    if is_harvest:
        results.append({"name": name, "status": "GRANJA_EL_HERAMI", "cat": cat, "qty": qty, "unit": unit})
        continue

    # Find matching pantry
    matched = []
    for p_key, p_obj in pantry_items.items():
        if p_obj["status"] != "canonical": continue
        if are_equivalent(p_obj["name"], name):
            matched.append(p_obj)

    results.append({
        "name": name,
        "cat": cat,
        "qty": qty,
        "unit": unit,
        "matched_pantry": [m["name"] for m in matched],
        "match_count": len(matched)
    })

# Analyze anomalies:
print("\n--- ANOMALIES & MATCH REPORT ---")
double_matches = [r for r in results if r.get("match_count", 0) > 1]
print(f"Items matching MULTIPLE pantry SKUs: {len(double_matches)}")
for d in double_matches:
    print(f"  * {d['name']} matched: {d['matched_pantry']}")

# Check Proteínas / Carnes
print("\n--- PROTEINAS / CARNES INGREDIENT AUDIT ---")
for r in results:
    if "Carnes" in r.get("cat", "") or "Pescados" in r.get("cat", ""):
        print(f"  {r['name']:35s} -> Pantry: {r.get('matched_pantry')} (Status: {r.get('status', 'MARKET')})")

