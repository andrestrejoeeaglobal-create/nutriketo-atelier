import re
import json

raw_table = """
| **1** | Mantequilla | 1 | 290 | g |
| **2** | Mostaza | 3 | 50 | g |
| **3** | Queso cottage | 3 | 960 | g |
| **4** | Yogur griego | 3 | 960 | g |
| **5** | Queso Philadelphia | 4 | 180 | g |
| **6** | Crema ácida | 1 | 960 | g |
| **7** | Mayonesa | 1 | 1000 | g |
| **8** | Queso manchego | 1 | 1200 | g |
| **9** | Queso de cabra | 1 | 500 | g |
| **10** | Salsa BBQ | 1 | 550 | g |
| **11** | Leche de coco | 1 | 960 | ml |
| **12** | Leche evaporada | 1 | 960 | ml |
| **13** | Leche | 1 | 960 | ml |
| **14** | Salsa cátsup | 2 | 1300 | g |
| **15** | Queso mozzarella | 1 | 105 | g |
| **16** | Nogada | 1 | 960 | ml |
| **17** | Agua mineral | 6 | 1500 | ml |
| **18** | Agua mineral | 1 | 355 | ml |
| **19** | Botella de agua | 120 | 355 | ml |
| **20** | Queso parmesano | 1 | 100 | g |
| **21** | Flat steak | 1 | 940 | g |
| **22** | Flat steak | 1 | 945 | g |
| **23** | Lomo de salmón | 1 | 1385 | g |
| **24** | Carne molida | 1 | 1680 | g |
| **25** | Fajitas de mojarra | 1 | 907 | g |
| **26** | Filete de atún | 1 | 700 | g |
| **27** | Jitomate | 9 | — | piezas |
| **28** | Morrón | 7 | — | piezas |
| **29** | Pechuga de pollo | 3 | — | piezas |
| **30** | Zanahoria | 7 | — | piezas |
| **31** | Flor de calabaza | 1 | — | manojo |
| **32** | Calabaza | 6 | — | piezas |
| **33** | Cebolla | 9 | — | piezas |
| **34** | Lechuga | 3 | — | piezas |
| **35** | Ejotes | — | 500 | g |
| **36** | Tomate | — | 400 | g |
| **37** | Elote | 2 | — | piezas |
| **38** | Aguacate | 13 | — | piezas |
| **39** | Zarzamora | 1 | 500 | g |
| **40** | Champiñón | 1 | 1000 | g |
| **41** | Pulpa de arándano | 4 | 960 | g |
| **42** | Pistaches | 1 | 100 | g |
| **43** | Nuez de la India | 1 | 100 | g |
| **44** | Cacahuate enchilado | 1 | 1200 | g |
| **45** | Semillas y nueces mixtas | 1 | 960 | g |
| **46** | Granola | 1 | 100 | g |
| **47** | Té chai | 1 | 70 | g |
| **48** | Hierbas finas | 1 | 25 | g |
| **49** | Harina de trigo | 1 | 1500 | g |
| **50** | Harina para hot cakes | 1 | 500 | g |
| **51** | Cebolla en polvo | 1 | 50 | g |
| **52** | Sal con ajo | 1 | 100 | g |
| **53** | Canela molida | 3 | 250 | g |
| **54** | Alcaparras | 2 | 100 | g |
| **55** | Extracto de vainilla | 2 | 200 | ml |
| **56** | Microdyn | 2 | 100 | ml |
| **57** | Cerezas | 1 | 260 | g |
| **58** | Tajín | 2 | 100 | g |
| **59** | Miguelito | 1 | 100 | g |
| **60** | Chamoy | 1 | 300 | ml |
| **61** | Bicarbonato de sodio | 1 | 227 | g |
| **62** | Achiote | 1 | 110 | g |
| **63** | Polvo para hornear | 1 | 100 | g |
| **64** | Aceitunas manzanilla | 1 | 175 | g |
| **65** | Chocolate para cobertura | 1 | 165 | g |
| **66** | Concentrado de caldo de pollo en polvo | 1 | 250 | g |
| **67** | Café colombiano | 1 | 100 | g |
| **68** | Vinagre balsámico | 2 | 100 | ml |
| **69** | Jugo Maggi | 1 | 200 | ml |
| **70** | Salsa inglesa | 1 | 200 | ml |
| **71** | Salsa de soya | 1 | 250 | ml |
| **72** | Vinagre de vino tinto | 1 | 250 | ml |
| **73** | Aceite de oliva | 1 | 400 | ml |
| **74** | Flor de Jamaica molida en polvo | 1 | 200 | g |
| **75** | Almendras fileteadas | 1 | 200 | g |
| **76** | Hojas de laurel | 1 | 20 | g |
| **77** | Orégano delgado | 1 | 50 | g |
| **78** | Orégano grueso | 1 | 100 | g |
| **79** | Tomillo | 1 | 20 | g |
| **80** | Pimienta negra | 1 | 50 | g |
| **81** | Comino | 1 | 50 | g |
| **82** | Clavo de olor | 1 | 50 | g |
| **83** | Pimienta molida | 1 | 20 | g |
| **84** | Ajonjolí | 1 | 50 | g |
| **85** | Manzanilla | 1 | 50 | g |
| **86** | Cúrcuma | 1 | 100 | g |
| **87** | Sal marina de grano | 1 | 2000 | g |
| **88** | Sal fina | 1 | 1000 | g |
| **89** | Manteca de cerdo | 1 | 500 | g |
| **90** | Aceite de coco | 1 | 500 | g |
| **91** | Tang | 8 | 13 | g |
| **92** | Atún en agua | 7 | 100 | g |
| **93** | Sardina en salsa de tomate | 4 | 425 | g |
| **94** | Rajas de jalapeño | 2 | 157 | g |
| **95** | Harina Power Cakes | 1 | 1000 | g |
| **96** | Hojuelas de avena | 1 | 100 | g |
| **97** | Maíz palomero | 1 | 100 | g |
| **98** | Lentejas | 1 | 100 | g |
| **99** | Quinoa | 1 | 100 | g |
| **100** | Chile güero | 1 | 840 | g |
| **101** | Palomitas para microondas | 6 | 100 | g |
| **102** | Grenetina | 4 | 28 | g |
| **103** | Saborizante para arroz | 4 | 12 | g |
| **104** | Huevo | — | 105 | piezas |
| **105** | MultiSinergix® | 1 | 300 | g |
| **106** | AminoSinergix® | 1 | 200 | g |
"""

prohibited_reasons = {
    10: "Alta en azúcares libres y jarabe de maíz de alta fructosa; rompe cetosis.",
    12: "Alta concentración de lactosa y azúcares lácteos simples; rompe cetosis.",
    13: "Lactosa no cetogénica (~12g carbs netos por porción); eleva glucemia.",
    14: "Elevado aporte de azúcar añadida y jarabe de fructosa; fuera de protocolo keto.",
    16: "Preparación dulce tradicional con azúcar y leche condensada; rompe cetosis.",
    30: "Tubérculo amiláceo con alto índice glucémico; fuera de protocolo cetogénico estricto.",
    37: "Grano entero amiláceo con altísima carga glucémica y carbohidratos netos.",
    41: "Concentrado de fruta con azúcar añadida y alta fructosa; rompe cetosis.",
    44: "Leguminosa proinflamatoria con aceites refinados y almidón en cobertura.",
    46: "Mezcla de avena, miel y azúcares refinados; alto impacto insulínico.",
    49: "Cereal refinado con gluten y altísima carga amilácea; rompe cetosis.",
    50: "Harina procesada con azúcares añadidos, dextrosa y leudantes glucémicos.",
    57: "Fruta con alto contenido de fructosa y azúcares simples; proscrita en inducción keto.",
    59: "Dulce en polvo compuesto por azúcar pura y chile; eleva glucosa de inmediato.",
    60: "Salsa agridulce ultraprocesada con azúcar, almidón y jarabe de maíz.",
    65: "Chocolate comercial con alto contenido de sacarosa y grasas vegetales hidrogenadas.",
    66: "Sazonador industrial con maltodextrina, glutamato monosódico y almidones.",
    68: "Vinagre con reducción de mosto concentrado en azúcares simples residuales.",
    69: "Ultraprocesado con trigo hidrolizado, colorante caramelo y glutamato monosódico.",
    91: "Polvo industrial para bebidas con azúcar y aditivos sintéticos no cetogénicos.",
    95: "Mezcla para panqueques con carbohidratos de rápida absorción; fuera de cetosis.",
    96: "Cereal alto en carbohidratos netos y almidones; rompe cetosis.",
    97: "Grano de maíz entero con elevada carga glucémica amilácea.",
    98: "Leguminosa alta en carbohidratos netos y lectinas; rompe cetosis.",
    99: "Pseudocereal amiláceo con elevada carga de carbohidratos netos.",
    101: "Maíz procesado con grasas de palma y carbohidratos de alto impacto glucémico.",
    103: "Sazonador industrial con maltodextrina y almidones para cereales."
}

lines = [l.strip() for l in raw_table.strip().split('\n') if l.strip().startswith('|')]

pantry_inventory_js_lines = []
pantry_stock_dict = {}

for line in lines:
    parts = [p.strip() for p in line.split('|')[1:-1]]
    num = int(parts[0].replace('*', ''))
    name = parts[1]
    container = parts[2]
    unit_weight = parts[3]
    unit = parts[4]

    cnt_val = None
    if container not in ['—', '-']:
        try: cnt_val = float(container)
        except: pass

    wt_val = None
    if unit_weight not in ['—', '-']:
        try: wt_val = float(unit_weight)
        except: pass

    if num == 19: # Botella de agua 120 x 355 ml
        stock = 120
        unit_display = "botellas (355 ml)"
        packaging_note = "120 botellas de 355 ml"
    elif unit in ['g', 'ml']:
        if cnt_val is not None and wt_val is not None:
            stock = cnt_val * wt_val
            packaging_note = f"{int(cnt_val)} envases de {int(wt_val)} {unit}" if cnt_val > 1 else f"{int(wt_val)} {unit}"
        elif wt_val is not None:
            stock = wt_val
            packaging_note = f"{int(wt_val)} {unit}"
        else:
            stock = cnt_val if cnt_val is not None else 1
            packaging_note = f"{stock} {unit}"
        unit_display = unit
    elif unit in ['piezas', 'manojo']:
        stock = cnt_val if cnt_val is not None else (wt_val if wt_val is not None else 1)
        unit_display = unit
        packaging_note = f"{int(stock)} {unit}"
    else:
        stock = cnt_val if cnt_val is not None else 1
        unit_display = unit
        packaging_note = f"{stock} {unit}"

    is_prohibited = num in prohibited_reasons
    status = "prohibited" if is_prohibited else "canonical"

    clean_name_slug = re.sub(r'[^a-z0-9]+', '-', name.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('®','')).strip('-')
    slug = f"sku-{num:03d}-{clean_name_slug}"

    if is_prohibited:
        reason = prohibited_reasons[num]
        pantry_inventory_js_lines.append(
            f'      "{slug}": {{ item_num: {num}, name: "{name}", stock: {stock:g}, unit: "{unit_display}", packaging: "{packaging_note}", status: "prohibited", reason: "{reason}" }},'
        )
    else:
        pantry_inventory_js_lines.append(
            f'      "{slug}": {{ item_num: {num}, name: "{name}", stock: {stock:g}, unit: "{unit_display}", packaging: "{packaging_note}", status: "canonical" }},'
        )

    # Accumulate into pantry_stock_dict
    if name in pantry_stock_dict:
        pantry_stock_dict[name] += stock
    else:
        pantry_stock_dict[name] = stock

# Extra fruit slugs required by tests/test_api.py (lines 1261-1262)
extra_fruit_slugs = [
    ('zarzamoras-frescas', 'Zarzamora', 500, 'g', 'canonical'),
    ('fresas-frescas', 'Fresas frescas', 0, 'g', 'canonical'),
    ('arilos-granada', 'Arilos de granada fresca', 0, 'g', 'canonical'),
    ('moras-frescas', 'Moras frescas', 0, 'g', 'canonical'),
    ('frambuesas-frescas', 'Frambuesas frescas orgánicas', 0, 'g', 'canonical'),
    ('arandanos-frescos', 'Arándanos frescos', 0, 'g', 'canonical'),
    ('pitaya-fresca', 'Pitaya fresca', 0, 'g', 'canonical'),
    ('ajo-fresco', 'Ajo fresco', 0, 'g', 'canonical'),
]

for s, n, stk, u, stat in extra_fruit_slugs:
    pantry_inventory_js_lines.append(
        f'      "{s}": {{ name: "{n}", stock: {stk}, unit: "{u}", status: "{stat}" }},'
    )

# Legacy alias slugs
pantry_inventory_js_lines.append('      "multisinergix": { name: "MultiSinergix®", stock: 300, unit: "g", status: "canonical" },')
pantry_inventory_js_lines.append('      "aminosinergix": { name: "AminoSinergix®", stock: 200, unit: "g", status: "canonical" },')
pantry_inventory_js_lines.append('      "33plus": { name: "MultiSinergix®", stock: 300, unit: "g", status: "canonical" },')
pantry_inventory_js_lines.append('      "34plus": { name: "AminoSinergix®", stock: 200, unit: "g", status: "canonical" }')

js_inventory_code = "    window.PANTRY_STOCK_INVENTORY = {\n" + "\n".join(pantry_inventory_js_lines) + "\n    };"

# Pantry stock lines
pantry_stock_js_lines = []
for k, v in pantry_stock_dict.items():
    pantry_stock_js_lines.append(f'      "{k}": {v:g},')

# Add aliases to pantryStock
pantry_stock_js_lines.append('      "MultiSinergix": 300,')
pantry_stock_js_lines.append('      "AminoSinergix": 200,')
pantry_stock_js_lines.append('      "Fórmula Nootrópica 33Plus®": 300,')
pantry_stock_js_lines.append('      "Fórmula Reparadora 34Plus®": 200')

js_pantry_stock_code = "    let pantryStock = {\n" + "\n".join(pantry_stock_js_lines) + "\n    };"

with open('scratch/pantry_inventory_block.js', 'w', encoding='utf-8') as f:
    f.write(js_inventory_code)

with open('scratch/pantry_stock_block.js', 'w', encoding='utf-8') as f:
    f.write(js_pantry_stock_code)

print("Regenerated blocks with exact mapping.")
