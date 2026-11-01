import json
import re
import unicodedata

def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

from test_refined_pairs import are_equivalent_v2, item_keywords
from test_slug_106 import normalize_slug_v2, canonical_map

with open("generate_standalone_html.py", "r", encoding="utf-8") as f:
    text = f.read()

# Load week 41
with open("semana_41_master.json", "r", encoding="utf-8") as f:
    s41 = json.load(f)

# Pantry 106 items
pantry_match = re.search(r"window\.PANTRY_STOCK_INVENTORY\s*=\s*(\{[\s\S]*?\n\s*\});", text)
pantry_items = {}
for m in re.finditer(r'"(sku-\d+-[^"]+)":\s*\{\s*item_num:\s*(\d+),\s*name:\s*"([^"]+)",\s*stock:\s*([\d\.]+),\s*unit:\s*"([^"]+)",\s*packaging:\s*"([^"]+)",\s*status:\s*"([^"]+)"', pantry_match.group(1)):
    pantry_items[m.group(1)] = {
        "sku": m.group(1),
        "item_num": int(m.group(2)),
        "name": m.group(3),
        "stock": float(m.group(4)),
        "unit": m.group(5),
        "packaging": m.group(6),
        "status": m.group(7)
    }

def get_piece_gram_weight(name):
    n = strip_accents(name)
    if "morron" in n or "pimiento" in n: return 160
    if ("pechuga" in n and "pollo" in n) or (re.search(r'\bpollo\b', n) and "pavo" not in n): return 500
    if ("calabacita" in n or "calabaza" in n) and "flor" not in n: return 180
    if "flor de calabaza" in n: return 180
    if "lechuga" in n: return 380
    if "jitomate" in n or "tomate saladet" in n: return 120
    if "cebolla" in n and "polvo" not in n: return 150
    if "zanahoria" in n: return 120
    if "aguacate" in n: return 180
    if "sardina" in n: return 425
    if "atun" in n: return 100
    return 1

def parse_qty_in_base(qty, unit_str):
    u = (unit_str or "").lower().strip()
    num = float(qty)
    if "kg" in u or "kilo" in u:
        return {"val": num * 1000 if num < 50 else num, "type": "mass", "baseUnit": "g"}
    if "ml" in u:
        return {"val": num, "type": "vol", "baseUnit": "ml"}
    if "g" in u or "gramo" in u:
        return {"val": num, "type": "mass", "baseUnit": "g"}
    if u in ["l", "lt", "lts", "litro", "litros"]:
        return {"val": num * 1000 if num < 50 else num, "type": "vol", "baseUnit": "ml"}
    return {"val": num, "type": "count", "baseUnit": u or "piezas"}

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

harvest_list = ["Espinacas frescas", "Calabacitas verdes tiernas", "Brócoli fresco", "Espárragos verdes", "Nopales tiernos", "Ejotes frescos", "Cilantro fresco", "Arúgula fresca", "Coliflor fresca", "Limones agrios frescos de la granja", "Nuez pecana fresca de la granja"]

shopping_result = []
for key, item in consolidated.items():
    name = item["name"]
    qty = item["quantity"]
    unit = item["unit"]
    cat = item["category"]

    if any(are_equivalent_v2(h, name) for h in harvest_list) or "Cosecha" in cat:
        shopping_result.append({"name": name, "cat": cat, "status": "GRANJA ($0)", "por_comprar": 0})
        continue

    yield_factor = 1.15 if ("Carnes" in cat or "Pescados" in cat) else (1.10 if "Verduras" in cat else 1.0)
    gross = qty * yield_factor
    base_info = parse_qty_in_base(gross, unit)

    stock_in_base = 0
    matched_pantry_name = None
    for p_key, p_obj in pantry_items.items():
        if p_obj["status"] != "canonical": continue
        if are_equivalent_v2(p_obj["name"], name):
            matched_pantry_name = p_obj["name"]
            parsed_stock = parse_qty_in_base(p_obj["stock"], p_obj["unit"])
            if base_info["type"] == 'mass' and parsed_stock["type"] == 'count':
                pw = get_piece_gram_weight(name)
                parsed_stock["val"] *= pw
                parsed_stock["type"] = 'mass'
            elif base_info["type"] == 'count' and parsed_stock["type"] == 'mass':
                pw = get_piece_gram_weight(name)
                parsed_stock["val"] = (parsed_stock["val"] / pw) if pw > 0 else parsed_stock["val"]
                parsed_stock["type"] = 'count'
            stock_in_base += parsed_stock["val"]

    net_needed = max(0, base_info["val"] - stock_in_base)
    status = "100% ALACENA ($0)" if net_needed <= 0 else ("PARCIAL ALACENA" if stock_in_base > 0 else "POR COMPRAR")
    shopping_result.append({
        "name": name,
        "cat": cat,
        "gross": base_info["val"],
        "unit": base_info["baseUnit"],
        "alacena": stock_in_base,
        "net": net_needed,
        "matched": matched_pantry_name,
        "status": status
    })

print("\n--- CRITICAL ITEMS AUDIT ---")
for r in shopping_result:
    if any(k in r["name"].lower() for k in ["sardina", "pavo", "pollo", "atun", "sal de mar", "morron", "mineral"]):
        print(f"[{r['status']:20s}] {r['name']:35s} | Bruto: {r['gross']:.1f} {r['unit']} | Alacena: {r['alacena']:.1f} | Net: {r['net']:.1f} | Matched: {r['matched']}")

