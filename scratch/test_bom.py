# -*- coding: utf-8 -*-
import json
from app.services.inventory_master import consolidate_market_bom

master = json.load(open("semana_40_master.json", encoding="utf-8"))
all_ings = []
for day in master["days"]:
    for meal in day["meals"]:
        for course in ["starter", "main", "side"]:
            all_ings.extend(meal[course].get("ingredients", []))

bom = consolidate_market_bom(all_ings)
print(f"Total BOM items: {len(bom)}")
for b in bom:
    n = b["name"].lower()
    if any(k in n for k in ["huevo", "portobello", "almendra", "limon"]):
        print(f"[{b['category']}] {b['name']}: {b['quantity']} {b['unit']}")
