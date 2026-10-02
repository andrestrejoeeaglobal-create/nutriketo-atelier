import sys, os, json
sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')
from app.services.inventory_master import consolidate_market_bom

master = json.load(open('semana_40_master.json', encoding='utf-8'))
all_ings = []
for d in master.get('days', []):
    for m in d.get('meals', []):
        for c in [m.get('starter'), m.get('main'), m.get('side')]:
            if c and isinstance(c, dict) and 'ingredients' in c:
                all_ings.extend(c['ingredients'])

bom = consolidate_market_bom(all_ings)

def getSmartItemCategory(itemName, explicitCategory):
    name = (itemName or '').lower().strip()
    # 0.0 Inmunidad Taxonómica: Aceites vegetales y grasas de cocción nunca son Quesos ni Lácteos
    if any(k in name for k in ['aceite', 'vevo', 'ajonjol', 'mantequilla', 'ghee']):
        return '🥑 Grasas, Aceites y Semillas'
    
    if explicitCategory and isinstance(explicitCategory, str) and explicitCategory.strip():
        ec = explicitCategory.strip()
        if 'Verduras' in ec or 'Hortalizas' in ec: return '🥬 Verduras, Hortalizas y Frescos'
        if 'Carnes' in ec or 'Pescados' in ec or 'Proteínas' in ec: return '🥩 Carnes, Pescados y Proteínas'
        if 'Frutas' in ec: return '🍓 Frutas de Bajo Índice Glucémico'
        if 'Quesos' in ec or ('Lácteos' in ec and 'Grasas' not in ec): return '🧀 Lácteos y Quesos (Sin Gluten — Keto)'
        if 'Grasas' in ec or 'Aceites' in ec or 'Semillas' in ec: return '🥑 Grasas, Aceites y Semillas'
        if 'Suplementación' in ec or 'Biotecnología' in ec or 'Bases Hidrocoloides' in ec: return '💊 SUPLEMENTACIÓN CELULAR — BIOTECNOLOGÍA'
        if 'Cítricos' in ec or 'Ácidos' in ec: return '🍋 Cítricos y Ácidos Naturales'
        if 'Especias' in ec or 'Hierbas' in ec or 'Aromáticos' in ec or 'Condimentos' in ec: return '🌶️ Chiles, Condimentos e Infusiones'
    return 'OTHER'

cards = {}
for it in bom:
    cat = getSmartItemCategory(it['name'], it['category'])
    cards.setdefault(cat, []).append(it)

print('=== 🧀 LÁCTEOS Y QUESOS ===')
for it in cards.get('🧀 Lácteos y Quesos (Sin Gluten — Keto)', []):
    print(f"  - {it['name']} ({it['quantity']} {it['unit']})")

print('\n=== 🥑 GRASAS, ACEITES Y SEMILLAS ===')
for it in cards.get('🥑 Grasas, Aceites y Semillas', []):
    print(f"  - {it['name']} ({it['quantity']} {it['unit']})")
