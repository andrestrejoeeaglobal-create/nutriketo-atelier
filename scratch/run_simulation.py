import sys
sys.path.append('scratch')
from test_classifier import resolve_to_canonical_sku, all_ings, RAW_PIECE_YIELD_GRAMS
import math

commodities = {}
house_preps = {}
solvents = {}

for ing in all_ings:
    name = ing.get('name', '')
    nl = name.lower()
    qty = float(ing.get('amount') or ing.get('quantity') or ing.get('base_qty', 1.0))
    unit = str(ing.get('unit', 'g')).strip().lower()

    if any(k in nl for k in ['agua purificada', 'agua para hidrataci', 'hielo']):
        # Utility solvent
        key = 'Agua purificada de cocina y mesa (red / garrafón)'
        if key not in solvents:
            solvents[key] = {'name': key, 'category': 'Suministros Operativos de Red', 'quantity': 0.0, 'unit': 'ml'}
        solvents[key]['quantity'] += qty
        continue

    if any(k in nl for k in ['caldo claro', 'caldo de ', 'caldo concentrado', 'fondo claro', 'infusi']):
        # House prep
        if name not in house_preps:
            house_preps[name] = {'name': name, 'category': 'Fondos e Infusiones de Cocina', 'quantity': 0.0, 'unit': unit}
        house_preps[name]['quantity'] += qty
        continue

    # Commercial commodity
    canonical_name, category = resolve_to_canonical_sku(name)

    # Unit adjustments
    is_piece = unit in ['piezas', 'pieza', 'pz', 'piezas/persona']
    if 'zacate' in canonical_name.lower() and is_piece:
        qty = qty * 2.0  # 2g per piece
        unit = 'g'
        is_piece = False

    if canonical_name not in commodities:
        commodities[canonical_name] = {
            'name': canonical_name,
            'category': category,
            'quantity': 0.0,
            'unit': 'piezas' if is_piece else unit,
            'is_piece': is_piece
        }

    slug = canonical_name.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o')
    if 'aguacate' in slug and not commodities[canonical_name]['is_piece'] and unit == 'g':
        commodities[canonical_name]['quantity'] += qty / RAW_PIECE_YIELD_GRAMS['aguacate_hass_fresco']
        commodities[canonical_name]['unit'] = 'piezas'
        commodities[canonical_name]['is_piece'] = True
    elif commodities[canonical_name]['is_piece'] and unit == 'g' and 'aguacate' in slug:
        commodities[canonical_name]['quantity'] += qty / RAW_PIECE_YIELD_GRAMS['aguacate_hass_fresco']
    elif 'limon' in slug and unit in ['ml', 'g']:
        commodities[canonical_name]['quantity'] += qty / RAW_PIECE_YIELD_GRAMS['limon_fresco']
        commodities[canonical_name]['unit'] = 'piezas'
        commodities[canonical_name]['is_piece'] = True
    elif 'portobello' in slug and unit == 'g':
        commodities[canonical_name]['quantity'] += qty / RAW_PIECE_YIELD_GRAMS['champiñon_portobello']
        commodities[canonical_name]['unit'] = 'piezas'
        commodities[canonical_name]['is_piece'] = True
    elif 'lechuga' in slug and is_piece and qty >= 6:
        # 18 leaves -> 2 lettuces
        commodities[canonical_name]['quantity'] += qty / RAW_PIECE_YIELD_GRAMS['lechuga_orejona_cogollo']
        commodities[canonical_name]['unit'] = 'piezas'
        commodities[canonical_name]['is_piece'] = True
    else:
        commodities[canonical_name]['quantity'] += qty

# Salvaguarda B: Add stock materials from house_preps
commodities['Huesos y retazo de pollo orgánico para fondo'] = {
    'name': 'Huesos y retazo de pollo orgánico para fondo',
    'category': 'Carnes, Aves y Pescados',
    'quantity': 500.0,
    'unit': 'g',
    'is_piece': False
}
commodities['Huesos de res con tuétano para fondo'] = {
    'name': 'Huesos de res con tuétano para fondo',
    'category': 'Carnes, Aves y Pescados',
    'quantity': 500.0,
    'unit': 'g',
    'is_piece': False
}
commodities['Flores de jamaica orgánica deshidratada'] = {
    'name': 'Flores de jamaica orgánica deshidratada',
    'category': 'Especias, Hierbas y Aromáticos',
    'quantity': 120.0,
    'unit': 'g',
    'is_piece': False
}

print('=== TOTAL COMMERCIAL COMMODITIES ===')
print('Count:', len(commodities))

for cat in sorted(set(it['category'] for it in commodities.values())):
    print(f"\n--- {cat} ---")
    for it in sorted(commodities.values(), key=lambda x: x['name']):
        if it['category'] == cat:
            q = int(math.ceil(it['quantity'])) if it.get('is_piece') else int(it['quantity']) if it['quantity'].is_integer() else round(it['quantity'], 1)
            print(f"* {it['name']}: {q} {it['unit']}")

print('\n=== TOTAL SOLVENTS (SECCIÓN 3.2) ===')
for s in solvents.values():
    print(f"* {s['name']}: {s['quantity']/1000:.2f} L ({int(s['quantity'])} ml)")

print('\n=== TOTAL HOUSE PREPS (SECCIÓN 3.2) ===')
print('Unique house prep recipes:', len(house_preps))
for hp in house_preps.values():
    print(f"* {hp['name']}: {int(hp['quantity'])} {hp['unit']}")
