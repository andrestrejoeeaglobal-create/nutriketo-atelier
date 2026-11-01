import json
import re
import unicodedata

def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

# Refined itemKeywords with strict exclusions and sardina
item_keywords = [
    # Carnes, Aves y Pescados
    {'stem': 'pollo', 'aliases': ['pechuga de pollo', 'pechuga de pollo organica', 'pollo organico', 'pollo fresco', 'carne de pollo'], 'exclude': ['hueso', 'huesos', 'retazo', 'fondo', 'caldo', 'pavo']},
    {'stem': 'pavo', 'aliases': ['pavo', 'pechuga de pavo', 'pechuga de pavo artesanal', 'jamon de pavo'], 'exclude': ['pollo', 'tocino']},
    {'stem': 'tocino-pavo', 'aliases': ['tocino de pavo', 'tocino de pavo artesanal'], 'exclude': ['pollo']},
    {'stem': 'sardina', 'aliases': ['sardina', 'sardinas', 'sardina enlatada', 'sardinas enlatadas', 'sardina en salsa de tomate', 'sardinas en salsa de tomate', 'sardinas en tomate', 'lata de sardinas', 'latas de sardinas']},
    {'stem': 'atun-fresco', 'aliases': ['medallon de atun', 'medallones de atun', 'filete de atun', 'atun fresco', 'lomo de atun'], 'exclude': ['enlatado', 'en agua', 'en lata', 'lata']},
    {'stem': 'atun-lata', 'aliases': ['atun enlatado', 'atun en agua', 'atun en lata', 'lata de atun'], 'exclude': ['fresco', 'medallon', 'filete']},
    {'stem': 'salmon', 'aliases': ['salmon', 'lomo de salmon', 'filete de salmon', 'salmon fresco', 'salmon salvaje'], 'exclude': ['salsa']},
    {'stem': 'mojarra', 'aliases': ['mojarra', 'fajita de mojarra', 'fajitas de mojarra', 'tilapia', 'fajita de tilapia', 'fajitas de mojarra tilapia']},
    {'stem': 'carne-molida', 'aliases': ['carne molida', 'carne molida de res', 'carne molida de sirloin', 'molida de res']},
    {'stem': 'flat-steak', 'aliases': ['flat steak', 'flatsteak', 'bife plano']},
    {'stem': 'arrachera', 'aliases': ['arrachera', 'arrachera de res', 'arrachera limpia', 'corte magro de arrachera'], 'exclude': ['hamburguesa']},
    {'stem': 'ribeye', 'aliases': ['ribeye', 'corte magro de ribeye', 'ribeye de res premium']},
    {'stem': 'huevo', 'aliases': ['huevo', 'huevos', 'huevos enteros', 'huevos organicos', 'huevos frescos', 'huevos organicos de libre pastoreo', 'huevos organicos de pastoreo']},
    
    # Lácteos y Quesos
    {'stem': 'mantequilla', 'aliases': ['mantequilla', 'mantequilla de vaca', 'mantequilla de pastoreo', 'mantequilla sin sal'], 'exclude': ['ghee', 'clarificada']},
    {'stem': 'cottage', 'aliases': ['queso cottage', 'cottage']},
    {'stem': 'yogur-griego', 'aliases': ['yogur griego', 'yoghurt griego', 'yogur griego natural', 'yoghurt griego natural sin azucar', 'oikos']},
    {'stem': 'philadelphia', 'aliases': ['queso philadelphia', 'philadelphia', 'queso crema philadelphia']},
    {'stem': 'crema-acida', 'aliases': ['crema acida', 'crema entera', 'crema para batir'], 'exclude': ['queso crema']},
    {'stem': 'mayonesa', 'aliases': ['mayonesa', 'mayonesa casera', 'mayonesa keto']},
    {'stem': 'manchego', 'aliases': ['queso manchego', 'manchego maduro']},
    {'stem': 'cabra', 'aliases': ['queso de cabra', 'queso de cabra artesanal', 'cabra artesanal', 'queso de cabra suave artesanal']},
    {'stem': 'parmesano', 'aliases': ['queso parmesano', 'parmesano maduro', 'queso parmesano artesanal']},
    {'stem': 'mozzarella', 'aliases': ['queso mozzarella', 'mozzarella']},
    {'stem': 'gouda', 'aliases': ['queso gouda', 'gouda artesanal']},
    {'stem': 'panela', 'aliases': ['queso panela', 'panela artesanal']},

    # Verduras y Frescos
    {'stem': 'jitomate', 'aliases': ['jitomate', 'jitomates', 'saladet', 'jitomate saladet', 'jitomate saladet fresco', 'jitomate bola'], 'exclude': ['tomate verde', 'tomatillo']},
    {'stem': 'tomate-verde', 'aliases': ['tomate verde', 'tomate verde fresco', 'tomatillo', 'tomate'], 'exclude': ['jitomate', 'saladet', 'salsa']},
    {'stem': 'morron', 'aliases': ['morron', 'morrones', 'pimiento morron', 'pimientos morrones', 'pimientos morrones dulces', 'pimiento morron dulce']},
    {'stem': 'zanahoria', 'aliases': ['zanahoria', 'zanahorias']},
    {'stem': 'flor-calabaza', 'aliases': ['flor de calabaza', 'flores de calabaza']},
    {'stem': 'calabaza', 'aliases': ['calabaza', 'calabazas', 'calabacita', 'calabacitas', 'calabacitas verdes tiernas'], 'exclude': ['flor', 'pepita', 'semilla']},
    {'stem': 'cebolla-fresca', 'aliases': ['cebolla', 'cebollas', 'cebolla blanca', 'cebolla blanca fresca', 'cebolla morada'], 'exclude': ['en polvo']},
    {'stem': 'cebolla-polvo', 'aliases': ['cebolla en polvo']},
    {'stem': 'lechuga', 'aliases': ['lechuga', 'lechugas', 'lechuga orejona', 'lechuga sweet', 'hojas de lechuga', 'hojas de lechuga orejona viva']},
    {'stem': 'ejote', 'aliases': ['ejote', 'ejotes', 'ejotes verdes', 'ejotes verdes tiernos']},
    {'stem': 'aguacate', 'aliases': ['aguacate', 'aguacates', 'aguacate hass', 'aguacate hass fresco']},
    {'stem': 'champinon', 'aliases': ['champinon', 'champinones', 'portobello', 'champinones portobello', 'champinones portobello frescos']},

    # Condimentos y Despensa
    {'stem': 'sal-mar', 'aliases': ['sal de mar', 'sal de colima', 'sal mineral', 'sal de mar mineral', 'sal marina de grano', 'sal fina'], 'exclude': ['salsa', 'ajo', 'salmon']},
    {'stem': 'sal-con-ajo', 'aliases': ['sal con ajo']},
    {'stem': 'ajo-fresco', 'aliases': ['ajo fresco', 'dientes de ajo', 'ajo machacado', 'ajo picado', 'ajo'], 'exclude': ['sal con ajo', 'ajonjoli']},
    {'stem': 'ajonjoli', 'aliases': ['ajonjoli', 'semillas de sesamo', 'semillas de ajonjoli'], 'exclude': ['aceite']},
    {'stem': 'manzanilla-te', 'aliases': ['manzanilla', 'flores de manzanilla', 'flores de manzanilla seca', 'te de manzanilla'], 'exclude': ['aceituna', 'aceitunas']},
    {'stem': 'aceitunas', 'aliases': ['aceitunas manzanilla', 'aceitunas', 'aceituna']},
    {'stem': 'alcaparras', 'aliases': ['alcaparras', 'alcaparra']},
    {'stem': 'canela', 'aliases': ['canela', 'canela molida', 'canela en polvo']},
    {'stem': 'oregano', 'aliases': ['oregano', 'oregano seco', 'oregano delgado', 'oregano grueso']},
    {'stem': 'tomillo', 'aliases': ['tomillo', 'tomillo fresco', 'tomillo seco']},
    {'stem': 'pimienta-negra', 'aliases': ['pimienta negra', 'pimienta negra molida', 'pimienta negra recien molida']},
    {'stem': 'curcuma', 'aliases': ['curcuma', 'curcuma en polvo', 'curry suave en polvo / curcuma']},
    {'stem': 'leche-coco', 'aliases': ['leche de coco', 'leche de coco sin azucar'], 'exclude': ['deshidratado', 'rallado', 'aceite']},
    {'stem': 'aceite-oliva', 'aliases': ['aceite de oliva', 'vevo', 'aceite de oliva extra virgen', 'aceite de oliva extra virgen vevo'], 'exclude': ['aceituna']},
    {'stem': 'agua-mineral', 'aliases': ['agua mineral', 'botellas de agua mineral', 'botella de agua mineral']},
    {'stem': 'agua-purificada', 'aliases': ['agua purificada', 'botella de agua', 'botellas de agua', 'agua pura'], 'exclude': ['mineral']},
    {'stem': 'multisinergix', 'aliases': ['multisinergix', 'multi sinergix', 'formula nootropica multisinergix', '33plus', '33 plus', 'formula nootropica 33plus']},
    {'stem': 'aminosinergix', 'aliases': ['aminosinergix', 'amino sinergix', 'formula reparadora aminosinergix', '34plus', '34 plus', 'formula reparadora 34plus']},
    {'stem': 'grenetina', 'aliases': ['grenetina', 'grenetina natural', 'grenetina natural en polvo']},
    {'stem': 'almendras', 'aliases': ['almendras', 'almendras fileteadas', 'almendras fileteadas tostadas']},
    {'stem': 'chia', 'aliases': ['chia', 'semillas de chia', 'semillas de chia organicas']},
    {'stem': 'girasol', 'aliases': ['semillas de girasol', 'semillas de girasol tostadas']},
    {'stem': 'calabaza-semillas', 'aliases': ['semillas de calabaza', 'semillas de calabaza tostadas', 'pepitas']},
    {'stem': 'vinagre-balsamico', 'aliases': ['vinagre balsamico', 'vinagre de manzana o balsamico']},
]

def are_equivalent_v2(a_name, b_name):
    if not a_name or not b_name: return False
    a = strip_accents(a_name).replace("nuex", "nuez")
    b = strip_accents(b_name).replace("nuex", "nuez")
    if a == b: return True

    for entry in item_keywords:
        if 'exclude' in entry and entry['exclude']:
            if any(ex in a for ex in entry['exclude']) or any(ex in b for ex in entry['exclude']):
                continue
        a_match = any(alias in a for alias in entry['aliases'])
        b_match = any(alias in b for alias in entry['aliases'])
        if a_match and b_match:
            return True
    return False

# Now test specific pairs!
test_pairs = [
    ("Sardinas enlatadas", "Sardina en salsa de tomate", True),
    ("Pechuga de pavo artesanal", "Pechuga de pollo", False),
    ("Pechuga de pollo orgánica", "Pechuga de pollo", True),
    ("Sal de mar", "Sardina en salsa de tomate", False),
    ("Sal de mar", "Salsa inglesa", False),
    ("Sal de mar", "Sal marina de grano", True),
    ("Ajo fresco", "Sal con ajo", False),
    ("Ajo fresco", "Ajonjolí", False),
    ("Flores de manzanilla seca", "Aceitunas manzanilla", False),
    ("Flores de manzanilla seca", "Manzanilla", True),
    ("Medallón de Atún fresco", "Filete de atún", True),
    ("Medallón de Atún fresco", "Atún en agua", False),
    ("Atún enlatado", "Atún en agua", True),
    ("Cebolla blanca fresca", "Cebolla", True),
    ("Cebolla blanca fresca", "Cebolla en polvo", False),
    ("Jitomate Saladet fresco", "Jitomate", True),
    ("Tomate verde fresco", "Tomate", True),
    ("Pimientos morrones dulces", "Morrón", True),
    ("Fórmula Nootrópica 33Plus®", "MultiSinergix", True),
    ("Fórmula Reparadora 34Plus®", "AminoSinergix", True),
]

all_passed = True
print("--- RUNNING PAIR VERIFICATION ---")
for a, b, expected in test_pairs:
    res = are_equivalent_v2(a, b)
    ok = (res == expected)
    if not ok: all_passed = False
    print(f"[{'PASS' if ok else 'FAIL'}] '{a}' <-> '{b}' => {res} (expected {expected})")

print(f"\nALL PAIR TESTS PASSED: {all_passed}")
