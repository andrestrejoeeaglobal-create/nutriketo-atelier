import json
import re
import unicodedata

def strip_accents(s):
    if not s: return ""
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

# Refined INGREDIENT_CANONICAL_MAP_JS
canonical_map = {
    "aceite-oliva": ["aceite de oliva", "aceite de oliva extra virgen", "aceite vevo", "aceite de oliva extra virgen vevo", "aceite de oliva virgen extra"],
    "te-verde": ["te verde", "te verde organico", "matcha ceremonial", "te verde sencha"],
    "huevo-organico": ["huevo", "huevos", "huevos frescos", "huevos organicos", "huevos frescos organicos", "huevos frescos organicos de pastoreo", "huevos enteros", "huevos organicos de pastoreo"],
    "pechuga-pavo": ["pechuga de pavo", "pavo artesanal", "pechuga de pavo artesanal", "jamon de pavo"],
    "pechuga-pollo": ["pechuga de pollo", "pollo fresco", "pechuga de pollo fresca", "pechuga de pollo organica", "pollo organico", "muslos de pollo"],
    "sirloin-magro": ["carne molida de sirloin", "sirloin magro", "carne molida de sirloin magra"],
    "filete-res": ["filete de res", "filete de res magro", "ribeye", "sirloin", "medallones de mignon"],
    "huachinango-fresco": ["huachinango", "filete de huachinango", "filete de huachinango fresco", "filete de huachinango al horno"],
    "robalo-fresco": ["robalo", "filete de robalo", "filete de robalo fresco", "filete de robalo a la plancha"],
    "salmon-salvaje": ["salmon", "salmon salvaje", "filete de salmon fresco", "filete de salmon salvaje", "filete de salmon fresco con piel", "lomo de salmon"],
    "pescado-blanco": ["pescado blanco", "filete de pescado blanco", "filete de pescado blanco fresco"],
    "atun-fresco": ["atun fresco", "medallon de atun", "medallones de atun", "filete de atun", "lomo de atun", "medallon de atun fresco"],
    "atun-enlatado": ["atun enlatado", "atun en agua", "atun en lata", "lata de atun"],
    "sardinas": ["sardinas enlatadas", "sardina enlatada", "sardina en salsa de tomate", "sardinas en salsa de tomate", "sardina", "sardinas", "lata de sardinas", "latas de sardinas"],
    "queso-parmesano": ["queso parmesano", "parmesano maduro", "queso parmesano maduro", "queso parmesano artesanal"],
    "queso-manchego": ["queso manchego", "manchego maduro", "queso manchego maduro"],
    "queso-gouda": ["queso gouda", "gouda maduro", "queso gouda maduro", "queso gouda artesanal"],
    "queso-panela": ["queso panela", "panela fresco", "queso panela fresco", "queso panela artesanal"],
    "queso-cabra": ["queso de cabra", "cabra artesanal", "queso de cabra artesanal", "queso de cabra suave artesanal"],
    "queso-crema": ["queso crema", "queso crema artesanal"],
    "queso-philadelphia": ["queso philadelphia", "philadelphia"],
    "queso-cottage": ["queso cottage", "cottage"],
    "queso-mozzarella": ["queso mozzarella", "mozzarella"],
    "mantequilla-pastoreo": ["mantequilla", "mantequilla de vaca", "mantequilla de pastoreo", "mantequilla sin sal"],
    "jitomate-bola": ["jitomate", "jitomates", "jitomate bola", "jitomate bola jugoso", "jitomate saladet", "jitomate saladet fresco", "saladet"],
    "tomate-verde": ["tomate verde", "tomate verde fresco", "tomatillo", "tomates verdes", "tomate"],
    "morron": ["morron", "morrones", "pimiento morron", "pimientos morrones", "pimientos morrones dulces"],
    "flor-calabaza": ["flor de calabaza", "flores de calabaza"],
    "calabaza": ["calabaza", "calabazas", "calabacita", "calabacitas", "calabacitas verdes tiernas"],
    "almendras-fileteadas": ["almendras fileteadas tostadas", "almendras fileteadas", "almendras tostadas", "almendras enteras", "almendra", "almendras"],
    "semillas-chia": ["semillas de chia organicas", "semillas de chia", "chia"],
    "semillas-ajonjoli": ["semillas de sesamo", "semillas de ajonjoli", "ajonjoli"],
    "ajo-fresco": ["ajo fresco", "dientes de ajo fresco", "dientes de ajo", "ajo picado", "ajo machacado"],
    "sal-con-ajo": ["sal con ajo"],
    "limon-fresco": ["jugo de limon fresco recien exprimido", "jugo de limon fresco", "limon fresco recien exprimido", "limones frescos", "limon agrio"],
    "pimienta-negra": ["pimienta negra recien molida", "pimienta negra molida", "pimienta negra"],
    "cebolla-blanca": ["cebolla blanca fresca", "cebolla blanca", "cebolla", "cebollas"],
    "cebolla-polvo": ["cebolla en polvo"],
    "sal-mar": ["sal de mar", "sal de colima", "sal mineral", "sal de mar mineral de colima", "sal marina de grano", "sal fina"],
    "manzanilla-te": ["manzanilla", "flores de manzanilla", "flores de manzanilla seca", "te de manzanilla"],
    "aceitunas-manzanilla": ["aceitunas manzanilla", "aceitunas", "aceituna"],
    "yoghurt-griego": ["yoghurt griego natural sin azucar", "yoghurt griego", "yogurt griego", "yogur griego"],
    "mayonesa": ["mayonesa", "mayonesa casera", "mayonesa keto"],
    "leche-coco": ["leche de coco", "leche de coco sin azucar"],
    "multisinergix": ["multisinergix", "multi sinergix", "33plus", "33 plus", "formula nootropica 33plus", "formula nootropica multisinergix"],
    "aminosinergix": ["aminosinergix", "amino sinergix", "34plus", "34 plus", "formula reparadora 34plus", "formula reparadora aminosinergix"],
    "flat-steak": ["flat steak", "flatsteak", "bife plano"],
    "carne-molida": ["carne molida", "carne molida de res"],
    "fajitas-mojarra": ["fajitas de mojarra", "fajita de mojarra", "fajitas de mojarra tilapia", "tilapia"]
}

def normalize_slug_v2(raw_name):
    if not raw_name: return ""
    clean = raw_name.strip().lower()
    clean_no_acc = strip_accents(clean)

    # 1. Exact match
    for slug, aliases in canonical_map.items():
        for alias in aliases:
            a_clean = strip_accents(alias)
            if clean_no_acc == a_clean:
                return slug

    # 2. Multi-word phrase or boundary match
    for slug, aliases in canonical_map.items():
        for alias in aliases:
            a_clean = strip_accents(alias)
            if " " in a_clean:
                # Multi-word alias: check if contained with space or substring
                if a_clean in clean_no_acc or clean_no_acc in a_clean:
                    return slug
            else:
                # Single-word alias: require word boundary
                pattern = r'(?:\b|_)' + re.escape(a_clean) + r'(?:\b|_)'
                if re.search(pattern, clean_no_acc):
                    return slug

    sanitized = re.sub(r'[^a-z0-9\s-]', '', clean_no_acc).replace(' ', '-')
    return re.sub(r'-+', '-', sanitized).strip('-') or "insumo-general"

pantry_106 = [
    "Mantequilla", "Mostaza", "Queso cottage", "Yogur griego", "Queso Philadelphia",
    "Crema ácida", "Mayonesa", "Queso manchego", "Queso de cabra", "Salsa BBQ",
    "Leche de coco", "Leche evaporada", "Leche", "Salsa cátsup", "Queso mozzarella",
    "Nogada", "Agua mineral", "Botella de agua", "Queso parmesano",
    "Flat steak", "Lomo de salmón", "Carne molida", "Fajitas de mojarra", "Filete de atún",
    "Jitomate", "Morrón", "Pechuga de pollo", "Zanahoria", "Flor de calabaza",
    "Calabaza", "Cebolla", "Lechuga", "Ejotes", "Tomate", "Elote", "Aguacate",
    "Zarzamora", "Champiñón", "Pulpa de arándano", "Pistaches", "Nuez de la India",
    "Cacahuate enchilado", "Semillas y nueces mixtas", "Granola", "Té chai",
    "Hierbas finas", "Harina de trigo", "Harina para hot cakes", "Cebolla en polvo",
    "Sal con ajo", "Canela molida", "Alcaparras", "Extracto de vainilla", "Microdyn",
    "Cerezas", "Tajín", "Miguelito", "Chamoy", "Bicarbonato de sodio", "Achiote",
    "Polvo para hornear", "Aceitunas manzanilla", "Chocolate para cobertura",
    "Concentrado de caldo de pollo en polvo", "Café colombiano", "Vinagre balsámico",
    "Jugo Maggi", "Salsa inglesa", "Salsa de soya", "Vinagre de vino tinto",
    "Aceite de oliva", "Flor de Jamaica molida en polvo", "Almendras fileteadas",
    "Hojas de laurel", "Orégano delgado", "Orégano grueso", "Tomillo",
    "Pimienta negra", "Comino", "Clavo de olor", "Pimienta molida", "Ajonjolí",
    "Manzanilla", "Cúrcuma", "Sal marina de grano", "Sal fina", "Manteca de cerdo",
    "Aceite de coco", "Tang", "Atún en agua", "Sardina en salsa de tomate",
    "Rajas de jalapeño", "Harina Power Cakes", "Hojuelas de avena", "Maíz palomero",
    "Lentejas", "Quinoa", "Chile güero", "Palomitas para microondas", "Grenetina",
    "Saborizante para arroz", "Huevo", "MultiSinergix", "AminoSinergix"
]

print("--- AUDITING ALL 106 ITEMS WITH NEW SLUG NORMALIZATION ---")
collisions = []
for i, item in enumerate(pantry_106, 1):
    slug = normalize_slug_v2(item)
    clean = strip_accents(item)
    if "salsa" in clean and slug == "sal-mar":
        collisions.append(f"COLLISION: {item} -> {slug}")
    if item == "Sardina en salsa de tomate" and slug != "sardinas":
        collisions.append(f"COLLISION: {item} -> {slug} (expected 'sardinas')")
    if item == "Ajonjolí" and slug == "ajo-fresco":
        collisions.append(f"COLLISION: {item} -> {slug} (expected 'semillas-ajonjoli')")
    if item == "Aceitunas manzanilla" and slug == "manzanilla-te":
        collisions.append(f"COLLISION: {item} -> {slug} (expected 'aceitunas-manzanilla')")
    print(f"{i:3d}. {item:35s} -> {slug}")

print("\nTotal Collisions detected:", len(collisions))
for c in collisions:
    print("  *", c)
