import json
with open('semana_40_master.json', 'r', encoding='utf-8') as f:
    s40 = json.load(f)
from app.services.inventory_master import consolidate_market_bom
all_ings = []
for day in s40.get('days', []):
    for meal in day.get('meals', []):
        for part in ['starter', 'main', 'side']:
            if part in meal and isinstance(meal[part], dict):
                all_ings.extend(meal[part].get('ingredients', []))
bom = consolidate_market_bom(all_ings)
with open('scratch/bom_items.txt', 'w', encoding='utf-8') as out:
    out.write(f'Total BOM items: {len(bom)}\n')
    for item in sorted(bom, key=lambda x: str(x.get('category', '')) + x['name']):
        out.write(f"{item.get('category')}: {item['name']} - {item['quantity']} {item['unit']}\n")
print(f'Written {len(bom)} items to scratch/bom_items.txt')
